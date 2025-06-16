package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/gorilla/websocket"
	"github.com/rs/cors"
	"github.com/sirupsen/logrus"
)

var logger *logrus.Logger

// LokiEntry represents a log entry for Loki
type LokiEntry struct {
	Timestamp string `json:"ts"`
	Line      string `json:"line"`
}

// LokiStream represents a stream of logs for Loki
type LokiStream struct {
	Stream map[string]string `json:"stream"`
	Values [][]string        `json:"values"`
}

// LokiPayload represents the payload sent to Loki
type LokiPayload struct {
	Streams []LokiStream `json:"streams"`
}

// LokiHook is a custom logrus hook for Loki
type LokiHook struct {
	url      string
	username string
	password string
	labels   map[string]string
}

func NewLokiHook(url, username, password string, labels map[string]string) *LokiHook {
	return &LokiHook{
		url:      url,
		username: username,
		password: password,
		labels:   labels,
	}
}

func (hook *LokiHook) Fire(entry *logrus.Entry) error {
	line, err := entry.String()
	if err != nil {
		return err
	}

	// Create timestamp in nanoseconds since Unix epoch
	timestamp := fmt.Sprintf("%d", time.Now().UnixNano())

	payload := LokiPayload{
		Streams: []LokiStream{
			{
				Stream: hook.labels,
				Values: [][]string{
					{timestamp, line},
				},
			},
		},
	}

	jsonData, err := json.Marshal(payload)
	if err != nil {
		return err
	}

	req, err := http.NewRequest("POST", hook.url, bytes.NewBuffer(jsonData))
	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", "application/json")
	if hook.username != "" && hook.password != "" {
		req.SetBasicAuth(hook.username, hook.password)
	}

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	return nil
}

func (hook *LokiHook) Levels() []logrus.Level {
	return logrus.AllLevels
}

// RollData represents the dice roll information
type RollData struct {
	ServerID  string   `json:"server_id"`
	UserID    string   `json:"user_id"`
	ChannelID string   `json:"channel_id"`
	Rolls     []int    `json:"rolls"`
	Sides     string   `json:"sides"`
	Palette   []string `json:"palette"`
	Effect    string   `json:"effect"`
}

// WebSocket connection manager
type ConnectionManager struct {
	connections map[string]map[*websocket.Conn]bool // channel -> connections
	mutex       sync.RWMutex
}

func NewConnectionManager() *ConnectionManager {
	return &ConnectionManager{
		connections: make(map[string]map[*websocket.Conn]bool),
	}
}

func (cm *ConnectionManager) AddConnection(channel string, conn *websocket.Conn) {
	cm.mutex.Lock()
	defer cm.mutex.Unlock()
	
	if cm.connections[channel] == nil {
		cm.connections[channel] = make(map[*websocket.Conn]bool)
	}
	cm.connections[channel][conn] = true
	
	logger.WithFields(logrus.Fields{
		"channel": channel,
		"total_connections": len(cm.connections[channel]),
	}).Info("WebSocket connection added")
}

func (cm *ConnectionManager) RemoveConnection(channel string, conn *websocket.Conn) {
	cm.mutex.Lock()
	defer cm.mutex.Unlock()
	
	if cm.connections[channel] != nil {
		delete(cm.connections[channel], conn)
		remainingConnections := len(cm.connections[channel])
		if remainingConnections == 0 {
			delete(cm.connections, channel)
		}
		
		logger.WithFields(logrus.Fields{
			"channel": channel,
			"remaining_connections": remainingConnections,
		}).Info("WebSocket connection removed")
	}
}

func (cm *ConnectionManager) BroadcastToChannel(channel string, data []byte) {
	cm.mutex.RLock()
	defer cm.mutex.RUnlock()
	
	connections, exists := cm.connections[channel]
	if !exists {
		logger.WithField("channel", channel).Debug("No connections for channel")
		return
	}
	
	var closedConnections []*websocket.Conn
	sentCount := 0
	
	for conn := range connections {
		err := conn.WriteMessage(websocket.TextMessage, data)
		if err != nil {
			logger.WithError(err).Debug("Failed to send message to connection")
			closedConnections = append(closedConnections, conn)
		} else {
			sentCount++
		}
	}
	
	// Clean up closed connections
	for _, conn := range closedConnections {
		delete(connections, conn)
		conn.Close()
	}
	
	logger.WithFields(logrus.Fields{
		"channel": channel,
		"sent_to": sentCount,
		"closed": len(closedConnections),
	}).Info("Broadcasted message to channel")
}

var connManager *ConnectionManager

func initLogger() {
	logger = logrus.New()
	logger.SetLevel(logrus.DebugLevel)
	
	// Get Loki configuration from environment variables
	lokiURL := os.Getenv("LOKI_URL")
	lokiUsername := os.Getenv("LOKI_USERNAME")
	lokiPassword := os.Getenv("LOKI_PASSWORD")
	
	// If Loki is configured, add the custom Loki hook
	if lokiURL != "" && lokiPassword != "" {
		labels := map[string]string{
			"service":     "dice-websocket",
			"namespace":   "diceable",
			"environment": "production",
		}
		
		lokiHook := NewLokiHook(lokiURL, lokiUsername, lokiPassword, labels)
		logger.AddHook(lokiHook)
		logger.Info("Loki logging initialized successfully")
	} else {
		logger.Warn("Loki not configured (LOKI_URL or LOKI_PASSWORD missing), using console logging only")
	}
}

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		originSource := os.Getenv("ORIGIN_SOURCE")
		requestOrigin := r.Header.Get("Origin")

		// Remove scheme from requestOrigin if it exists
		if strings.HasPrefix(requestOrigin, "http://") {
			requestOrigin = strings.TrimPrefix(requestOrigin, "http://")
		} else if strings.HasPrefix(requestOrigin, "https://") {
			requestOrigin = strings.TrimPrefix(requestOrigin, "https://")
		}

		logger.WithFields(logrus.Fields{
			"request_origin": requestOrigin,
			"allowed_origin": originSource,
		}).Debug("Origin check")
		
		// Allow all origins if ORIGIN_SOURCE is not set (for development)
		if originSource == "" {
			return true
		}
		
		return requestOrigin == originSource
	},
}

func main() {
	// Initialize logger and connection manager
	initLogger()
	connManager = NewConnectionManager()
	logger.Info("Starting dice WebSocket service")

	port := os.Getenv("PORT")
	if port == "" {
		port = "5555"
	}
	
	originSource := os.Getenv("ORIGIN_SOURCE")
	logger.WithFields(logrus.Fields{
		"port": port,
		"allowed_origins": originSource,
	}).Info("Configuration loaded")

	// WebSocket endpoint for frontend connections
	http.HandleFunc("/ws/rolls/", handleWebSocket)
	
	// HTTP endpoint for receiving roll data from Discord bot
	http.HandleFunc("/api/roll/", handleRollAPI)
	
	// Health check endpoint
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	})

	// Set up CORS
	var corsHandler http.Handler
	if originSource != "" {
		corsHandler = cors.New(cors.Options{
			AllowedOrigins: []string{originSource},
			AllowedMethods: []string{"GET", "POST", "OPTIONS"},
			AllowedHeaders: []string{"*"},
		}).Handler(http.DefaultServeMux)
	} else {
		// Allow all origins for development
		corsHandler = cors.Default().Handler(http.DefaultServeMux)
	}

	logger.WithField("port", port).Info("Dice WebSocket service listening")

	if err := http.ListenAndServe(":"+port, corsHandler); err != nil {
		logger.WithError(err).Fatal("Failed to start server")
	}
}

func handleWebSocket(w http.ResponseWriter, r *http.Request) {
	// Extract channel ID from URL path: /ws/rolls/{channel}
	pathParts := strings.Split(r.URL.Path, "/")
	if len(pathParts) < 4 {
		logger.WithField("url_path", r.URL.Path).Error("Invalid WebSocket URL path")
		http.Error(w, "Invalid URL path", http.StatusBadRequest)
		return
	}
	
	channel := pathParts[3] // e.g., "roll-{user_id}"
	
	requestLogger := logger.WithField("channel", channel)
	requestLogger.Info("WebSocket connection request")

	// Upgrade to WebSocket
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		requestLogger.WithError(err).Error("Failed to upgrade to WebSocket")
		http.Error(w, "Failed to upgrade connection", http.StatusBadRequest)
		return
	}
	defer conn.Close()

	// Add connection to manager
	connManager.AddConnection(channel, conn)
	defer connManager.RemoveConnection(channel, conn)

	requestLogger.Info("WebSocket connection established")

	// Keep connection alive and handle ping/pong
	for {
		messageType, message, err := conn.ReadMessage()
		if err != nil {
			if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
				requestLogger.WithError(err).Error("WebSocket error")
			} else {
				requestLogger.Debug("WebSocket connection closed")
			}
			break
		}

		// Handle ping messages
		if messageType == websocket.TextMessage && string(message) == "ping" {
			err = conn.WriteMessage(websocket.TextMessage, []byte("pong"))
			if err != nil {
				requestLogger.WithError(err).Error("Failed to send pong")
				break
			}
			requestLogger.Debug("Responded to ping with pong")
		}
	}
}

func handleRollAPI(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Extract user ID from URL path: /api/roll/{user_id}
	pathParts := strings.Split(r.URL.Path, "/")
	if len(pathParts) < 4 {
		logger.WithField("url_path", r.URL.Path).Error("Invalid API URL path")
		http.Error(w, "Invalid URL path", http.StatusBadRequest)
		return
	}
	
	userID := pathParts[3]
	channel := fmt.Sprintf("roll-%s", userID)
	
	requestLogger := logger.WithFields(logrus.Fields{
		"user_id": userID,
		"channel": channel,
	})

	// Parse roll data
	var rollData RollData
	err := json.NewDecoder(r.Body).Decode(&rollData)
	if err != nil {
		requestLogger.WithError(err).Error("Failed to parse roll data")
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	requestLogger.WithFields(logrus.Fields{
		"sides": rollData.Sides,
		"rolls": rollData.Rolls,
		"effect": rollData.Effect,
	}).Info("Received dice roll")

	// Convert back to JSON for broadcasting
	messageData, err := json.Marshal(rollData)
	if err != nil {
		requestLogger.WithError(err).Error("Failed to marshal roll data")
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}

	// Broadcast to WebSocket clients
	connManager.BroadcastToChannel(channel, messageData)

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("OK"))
}
