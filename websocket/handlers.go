package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"

	"github.com/gorilla/websocket"
	"github.com/sirupsen/logrus"
)

// upgrader handles WebSocket upgrade with origin checking
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

		// Allow all origins if ORIGIN_SOURCE is not set (for development)
		if originSource == "" {
			return true
		}

		return requestOrigin == originSource
	},
}

// handleWebSocket handles WebSocket connection requests
func handleWebSocket(w http.ResponseWriter, r *http.Request, connManager *ConnectionManager, logger *logrus.Logger) {
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

// handleRollAPI handles API requests for dice rolls
func handleRollAPI(w http.ResponseWriter, r *http.Request, connManager *ConnectionManager, logger *logrus.Logger) {
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
		"sides":  rollData.Sides,
		"rolls":  rollData.Rolls,
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

// healthHandler handles health check requests
func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("OK"))
}
