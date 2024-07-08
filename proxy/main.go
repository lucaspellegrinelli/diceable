package main

import (
	"fmt"
	"github.com/gorilla/websocket"
	"github.com/rs/cors"
	"log"
	"net/http"
	"os"
	"strings"
)

var (
	upgrader = websocket.Upgrader{
		CheckOrigin: func(r *http.Request) bool {
			originSource := os.Getenv("ORIGIN_SOURCE")
			requestOrigin := r.Header.Get("Origin")

			// Remove scheme from requestOrigin if it exists
			if strings.HasPrefix(requestOrigin, "http://") {
				requestOrigin = strings.TrimPrefix(requestOrigin, "http://")
			} else if strings.HasPrefix(requestOrigin, "https://") {
				requestOrigin = strings.TrimPrefix(requestOrigin, "https://")
			}

			fmt.Printf("Request origin: %s, Allowed origin: %s\n", requestOrigin, originSource)
			return requestOrigin == originSource
		},
	}
)

func main() {
	port := "3000"
	suburbHost := os.Getenv("SUBURB_HOST")
	suburbToken := os.Getenv("SUBURB_TOKEN")
	originSource := os.Getenv("ORIGIN_SOURCE")

	fmt.Printf("Allowed origins: %s\n", originSource)

	if suburbHost == "" || suburbToken == "" || originSource == "" {
		log.Fatal("Environment variables SUBURB_HOST, SUBURB_TOKEN, and ORIGIN_SOURCE must be set")
	}

	http.HandleFunc("/rolls/", func(w http.ResponseWriter, r *http.Request) {
		handleWebSocketProxy(w, r, suburbHost, suburbToken)
	})

	// Set up CORS to allow only the specified origin
	corsHandler := cors.New(cors.Options{
		AllowedOrigins: []string{originSource},
	}).Handler(http.DefaultServeMux)

	log.Printf("Proxy listening on port %s", port)

	if err := http.ListenAndServe(":"+port, corsHandler); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}

func handleWebSocketProxy(w http.ResponseWriter, r *http.Request, suburbHost, suburbToken string) {
	// Extract the ID from the URL path
	pathParts := strings.Split(r.URL.Path, "/")
	if len(pathParts) < 3 {
		http.Error(w, "Invalid URL path", http.StatusBadRequest)
		return
	}
	id := pathParts[2]

	// Define the target URL
	targetURL := "wss://" + suburbHost + "/pubsub/" + id + "/listen"

	// Upgrade the incoming request to a WebSocket connection
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("Failed to upgrade connection: %v", err)
		return
	}
	defer conn.Close()

	// Connect to the target WebSocket server with the authorization header
	headers := http.Header{}
	headers.Add("authorization", suburbToken)

	targetConn, _, err := websocket.DefaultDialer.Dial(targetURL, headers)
	if err != nil {
		log.Printf("Failed to connect to target WebSocket server: %v", err)
		http.Error(w, "Failed to connect to target server", http.StatusInternalServerError)
		return
	}
	defer targetConn.Close()

	// Proxy messages between the client and the target server
	proxyWebSocket(conn, targetConn)
}

func proxyWebSocket(clientConn, targetConn *websocket.Conn) {
	done := make(chan struct{})

	go func() {
		defer clientConn.Close()
		defer targetConn.Close()
		for {
			messageType, message, err := clientConn.ReadMessage()
			if err != nil {
				log.Printf("Error reading from client: %v", err)
				break
			}
			if err := targetConn.WriteMessage(messageType, message); err != nil {
				log.Printf("Error writing to target: %v", err)
				break
			}
		}
		close(done)
	}()

	go func() {
		defer clientConn.Close()
		defer targetConn.Close()
		for {
			messageType, message, err := targetConn.ReadMessage()
			if err != nil {
				log.Printf("Error reading from target: %v", err)
				break
			}
			if err := clientConn.WriteMessage(messageType, message); err != nil {
				log.Printf("Error writing to client: %v", err)
				break
			}
		}
		close(done)
	}()

	<-done
}
