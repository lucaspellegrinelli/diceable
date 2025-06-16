import logging
import os
import time
from logging import LogRecord
from typing import Dict

import requests


class LokiHandler(logging.Handler):
    """Custom Loki handler that sends logs directly to Loki push API with minimal labels"""

    def __init__(self, url: str, username: str, password: str, labels: Dict[str, str]):
        super().__init__()
        self.url = url
        self.username = username
        self.password = password
        self.labels = labels
        self.session = requests.Session()
        self.session.timeout = 10

        if username and password:
            self.session.auth = (username, password)

    def emit(self, record: LogRecord):
        """Send log record to Loki"""
        try:
            log_message = self.format(record)
            timestamp = str(int(time.time() * 1000000000))
            payload = {
                "streams": [
                    {"stream": self.labels, "values": [[timestamp, log_message]]}
                ]
            }

            response = self.session.post(
                self.url, json=payload, headers={"Content-Type": "application/json"}
            )

            if response.status_code != 204:
                pass

        except Exception:
            pass


def setup_loki_logger():
    """Setup logger with custom Loki handler for centralized logging"""

    loki_url = os.getenv("LOKI_URL", "")
    loki_username = os.getenv("LOKI_USERNAME", "")
    loki_password = os.getenv("LOKI_PASSWORD", "")

    logger = logging.getLogger("diceable-discord-bot")

    if not loki_password:
        logger.warning(
            "LOKI_PASSWORD environment variable not set. Loki logging will be disabled."
        )
        # Setup console-only logging
        if not logger.hasHandlers():
            logger.setLevel(logging.DEBUG)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        return logger

    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        # Console handler for local development
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        def get_logger_level_name(level: int) -> str:
            return logging.getLevelName(level).lower()

        try:
            labels = {
                "service_name": "discord-bot",
                "namespace": "diceable",
                "environment": "production",
                "instance": "cloud",
                "level": get_logger_level_name(logger.level),
            }

            loki_handler = LokiHandler(
                url=loki_url,
                username=loki_username,
                password=loki_password,
                labels=labels,
            )
            loki_handler.setLevel(logging.DEBUG)
            loki_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
            logger.addHandler(loki_handler)
            logger.info("Loki logging initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Loki handler: {e}")
            logger.warning("Falling back to console logging only")

    return logger
