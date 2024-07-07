import logging
from logging import LogRecord

import requests


class SuburbClient:
    def __init__(self, namespace, host, api_key):
        self.namespace = namespace
        self.host = host
        self.headers = {
            "Authorization": f"{api_key}",
            "Content-Type": "application/json",
        }

        if self.host.endswith("/"):
            self.host = self.host[:-1]

    def create_queue(self, queue):
        data = {"namespace": self.namespace, "queue": queue}
        requests.post(f"{self.host}/queues", json=data, headers=self.headers)

    def push_to_queue(self, name, message):
        data = {"message": message}
        response = requests.post(
            f"{self.host}/queues/{self.namespace}/{name}",
            json=data,
            headers=self.headers,
        )
        return response.json()

    def pop_queue(self, name):
        requests.post(
            f"{self.host}/queues/{self.namespace}/{name}/pop", headers=self.headers
        )

    def add_log(self, source, level, message):
        data = {"source": source, "level": level, "message": message}
        response = requests.post(
            f"{self.host}/logs/{self.namespace}", json=data, headers=self.headers
        )
        return response.json()


class SuburbLogHandler(logging.Handler):
    def __init__(self, namespace: str, source: str, host: str, api_key: str):
        super().__init__()
        self.source = source
        self.suburb_client = SuburbClient(namespace, host, api_key)

        format = "%(message)s"
        self.setFormatter(logging.Formatter(format))

    def emit(self, record: LogRecord):
        log_entry = self.format(record)
        self.suburb_client.add_log(self.source, record.levelname, log_entry)


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


class SuburbQueue:
    def __init__(self, namespace: str, host: str, api_key: str):
        self.namespace = namespace
        self.host = host
        self.api_key = api_key
        self.client = SuburbClient(namespace, host, api_key)

    def push(self, name: str, message: str):
        self.client.create_queue(name)
        return self.client.push_to_queue(name, message)

    def pop(self, name: str):
        self.client.pop_queue(name)
