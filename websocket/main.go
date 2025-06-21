package main

import (
	"net/http"
	"os"

	"github.com/rs/cors"
	"github.com/sirupsen/logrus"
)

var (
	logger      *logrus.Logger
	connManager *ConnectionManager
)

func main() {
	// Initialize logger and connection manager
	logger = initLogger()
	connManager = NewConnectionManager()
	logger.Info("Starting dice WebSocket service")

	port := os.Getenv("PORT")
	if port == "" {
		port = "5555"
	}

	originSource := os.Getenv("ORIGIN_SOURCE")
	logger.WithFields(logrus.Fields{
		"port":            port,
		"allowed_origins": originSource,
	}).Info("Configuration loaded")

	// WebSocket endpoint for frontend connections
	http.HandleFunc("/ws/rolls/", func(w http.ResponseWriter, r *http.Request) {
		handleWebSocket(w, r, connManager, logger)
	})

	// HTTP endpoint for receiving roll data from Discord bot
	http.HandleFunc("/api/roll/", func(w http.ResponseWriter, r *http.Request) {
		handleRollAPI(w, r, connManager, logger)
	})

	// Health check endpoint
	http.HandleFunc("/health", healthHandler)

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
