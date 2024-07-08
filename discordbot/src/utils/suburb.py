import logging
import os
from logging import LogRecord

import requests


class SuburbWebsocket:
    def __init__(self, host: str, token: str):
        self.host = f"https://{host}"
        self.token = token
        self.headers = {"Authorization": self.token}

    def publish_message(self, channel: str, message: str):
        url = os.path.join(self.host, "pubsub", channel, "publish")
        requests.post(url, json={"message": message}, headers=self.headers)


class SuburbLogHandler(logging.Handler):
    def __init__(self, namespace: str, source: str, host: str, api_key: str):
        super().__init__()
        self.namespace = namespace
        self.source = source
        self.host = f"https://{host}"
        self.headers = {
            "Authorization": f"{api_key}",
            "Content-Type": "application/json",
        }

        format = "%(message)s"
        self.setFormatter(logging.Formatter(format))

    def emit(self, record: LogRecord):
        log_entry = self.format(record)
        data = {"source": self.source, "level": self.level, "message": log_entry}
        url = os.path.join(self.host, "logs", self.namespace)
        requests.post(url, json=data, headers=self.headers)


def setup_logger(namespace: str, source: str, host: str, api_key: str):
    logger = logging.getLogger(source)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        suburb_handler = SuburbLogHandler(namespace, source, host, api_key)
        suburb_handler.setLevel(logging.DEBUG)

        console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

        logger.addHandler(console_handler)
        logger.addHandler(suburb_handler)

    return logger
