package main

import (
    "log"
    "net/http"
    "os"
    "strings"

    "github.com/gorilla/websocket"
)

var (
    upgrader = websocket.Upgrader{}
)

func main() {
    port := "3000"
    suburbHost := os.Getenv("SUBURB_HOST")
    suburbToken := os.Getenv("SUBURB_TOKEN")

    if suburbHost == "" || suburbToken == "" {
        log.Fatal("Environment variables SUBURB_HOST and SUBURB_TOKEN must be set")
    }

    http.HandleFunc("/rolls/", func(w http.ResponseWriter, r *http.Request) {
        handleWebSocketProxy(w, r, suburbHost, suburbToken)
    })

    log.Printf("Proxy listening on port %s", port)

    if err := http.ListenAndServe(":"+port, nil); err != nil {
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
        defer close(done)
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
    }()

    go func() {
        defer close(done)
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
    }()

    <-done
}
