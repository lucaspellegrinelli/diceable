package main

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
