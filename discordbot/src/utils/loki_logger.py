import logging
import os

from logging_loki import LokiHandler


def setup_loki_logger(service_name: str, namespace: str = "diceable"):
    """Setup logger with Loki handler for centralized logging"""

    # Loki endpoint configuration from environment variables
    loki_url = os.getenv("LOKI_URL", "https://loki.ellep.dev/loki/api/v1/push")
    loki_username = os.getenv("LOKI_USERNAME", "default")
    loki_password = os.getenv("LOKI_PASSWORD")

    logger = logging.getLogger(service_name)

    # Check if Loki password is provided
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

        # Loki handler for centralized logging
        try:
            loki_handler = LokiHandler(
                url=loki_url,
                tags={
                    "service": service_name,
                    "namespace": namespace,
                    "environment": "production",
                },
                auth=(loki_username, loki_password),
                version="1",
            )
            loki_handler.setLevel(logging.DEBUG)
            logger.addHandler(loki_handler)
            logger.info(f"Loki logging initialized for service: {service_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Loki handler: {e}")
            logger.warning("Falling back to console logging only")

    return logger
