package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/sirupsen/logrus"
)

// LokiHook is a custom logrus hook for Loki
type LokiHook struct {
	url      string
	username string
	password string
	labels   map[string]string
}

// NewLokiHook creates a new Loki hook for logrus
func NewLokiHook(url, username, password string, labels map[string]string) *LokiHook {
	return &LokiHook{
		url:      url,
		username: username,
		password: password,
		labels:   labels,
	}
}

// Fire sends log entry to Loki
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

// Levels returns the available log levels
func (hook *LokiHook) Levels() []logrus.Level {
	return logrus.AllLevels
}

// initLogger initializes the logger with optional Loki integration
func initLogger() *logrus.Logger {
	logger := logrus.New()
	logger.SetLevel(logrus.DebugLevel)

	// Get Loki configuration from environment variables
	lokiURL := os.Getenv("LOKI_URL")
	lokiUsername := os.Getenv("TELEMETRY_USERNAME")
	lokiPassword := os.Getenv("TELEMETRY_PASSWORD")

	// If Loki is configured, add the custom Loki hook
	if lokiURL != "" && lokiPassword != "" {
		labels := map[string]string{
			"service_name": "websocket",
			"namespace":    "diceable",
			"environment":  "production",
			"instance":     "cloud",
			"level":        "debug",
		}

		lokiHook := NewLokiHook(lokiURL, lokiUsername, lokiPassword, labels)
		logger.AddHook(lokiHook)
		logger.Info("Loki logging initialized successfully")
	} else {
		logger.Warn("Loki not configured (LOKI_URL or TELEMETRY_PASSWORD missing), using console logging only")
	}

	return logger
}
