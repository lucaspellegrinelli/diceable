import logging

import requests


class DiceWebSocketPublisher:
    def __init__(self, websocket_host: str):
        """Initialize the dice WebSocket publisher

        Args:
            websocket_host: The host of the dice WebSocket service (e.g., "ws-proxy:3000")
        """
        self.host = f"http://{websocket_host}"
        self.logger = logging.getLogger("diceable-discord-bot")

    def publish_roll(self, user_id: str, roll_data: dict):
        """Publish dice roll data to the WebSocket service

        Args:
            user_id: The user ID to send the roll to
            roll_data: Dictionary containing roll information
        """
        url = f"{self.host}/api/roll/{user_id}"

        try:
            response = requests.post(
                url,
                json=roll_data,
                headers={"Content-Type": "application/json"},
                timeout=5,
            )

            if response.status_code == 200:
                self.logger.info(f"Successfully published roll data to {user_id}")
            else:
                self.logger.error(
                    f"Failed to publish roll data: HTTP {response.status_code}"
                )

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error publishing roll data: {e}")
            # Don't raise the exception - we don't want dice rolling to fail
            # if WebSocket publishing fails
