package main

import (
	"sync"

	"github.com/gorilla/websocket"
)

// ConnectionManager manages WebSocket connections organized by channels
type ConnectionManager struct {
	connections map[string]map[*websocket.Conn]bool // channel -> connections
	mutex       sync.RWMutex
}

// NewConnectionManager creates a new connection manager instance
func NewConnectionManager() *ConnectionManager {
	return &ConnectionManager{
		connections: make(map[string]map[*websocket.Conn]bool),
	}
}

// AddConnection adds a WebSocket connection to a specific channel
func (cm *ConnectionManager) AddConnection(channel string, conn *websocket.Conn) {
	cm.mutex.Lock()
	defer cm.mutex.Unlock()

	if cm.connections[channel] == nil {
		cm.connections[channel] = make(map[*websocket.Conn]bool)
	}
	cm.connections[channel][conn] = true
}

// RemoveConnection removes a WebSocket connection from a specific channel
func (cm *ConnectionManager) RemoveConnection(channel string, conn *websocket.Conn) {
	cm.mutex.Lock()
	defer cm.mutex.Unlock()

	if cm.connections[channel] != nil {
		delete(cm.connections[channel], conn)
		remainingConnections := len(cm.connections[channel])
		if remainingConnections == 0 {
			delete(cm.connections, channel)
		}
	}
}

// BroadcastToChannel sends data to all connections in a specific channel
func (cm *ConnectionManager) BroadcastToChannel(channel string, data []byte) {
	cm.mutex.RLock()
	defer cm.mutex.RUnlock()

	connections, exists := cm.connections[channel]
	if !exists {
		return
	}

	var closedConnections []*websocket.Conn

	for conn := range connections {
		err := conn.WriteMessage(websocket.TextMessage, data)
		if err != nil {
			closedConnections = append(closedConnections, conn)
		}
	}

	// Clean up closed connections
	for _, conn := range closedConnections {
		delete(connections, conn)
		conn.Close()
	}
}
