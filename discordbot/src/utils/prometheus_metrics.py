import os
import time
from contextlib import contextmanager
from typing import Optional

from prometheus_client import CollectorRegistry, Counter, Histogram, push_to_gateway
from prometheus_client.exposition import basic_auth_handler


class PrometheusMetrics:
    """Custom Prometheus metrics collector that pushes metrics to Prometheus Gateway"""

    def __init__(
        self,
        gateway_url: str,
        username: str,
        password: str,
        job_name: str = "discord-bot",
    ):
        self.gateway_url = gateway_url
        self.username = username
        self.password = password
        self.job_name = job_name
        self.registry = CollectorRegistry()

        # Initialize metrics
        self.gif_generation_time = Histogram(
            "gif_generation_duration_seconds",
            "Time spent generating GIFs in seconds",
            ["sides", "dice_count"],
            registry=self.registry,
        )

        self.gif_generation_count = Counter(
            "gif_generation_total",
            "Total number of GIFs generated",
            ["sides", "dice_count"],
            registry=self.registry,
        )

        self.roll_count = Counter(
            "dice_rolls_total",
            "Total number of dice rolls",
            ["sides", "dice_count"],
            registry=self.registry,
        )

    @contextmanager
    def time_gif_generation(self, sides: str, dice_count: int):
        """Context manager to time GIF generation"""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            self.gif_generation_time.labels(sides=sides, dice_count=dice_count).observe(
                duration
            )
            self.gif_generation_count.labels(sides=sides, dice_count=dice_count).inc()
            self._push_metrics()

    def record_roll(self, sides: str, dice_count: int):
        """Record a dice roll event"""
        self.roll_count.labels(sides=sides, dice_count=dice_count).inc()
        self._push_metrics()

    def _push_metrics(self):
        """Push metrics to Prometheus Gateway"""
        try:
            # Create authentication handler for basic auth
            def auth_handler(url, method, timeout, headers, data):
                return basic_auth_handler(
                    url, method, timeout, headers, data, self.username, self.password
                )

            push_to_gateway(
                self.gateway_url,
                job=self.job_name,
                registry=self.registry,
                handler=auth_handler,
            )
        except Exception:
            # Silently fail to avoid disrupting bot functionality
            pass


def setup_prometheus_metrics() -> Optional[PrometheusMetrics]:
    """Setup Prometheus metrics collector with gateway integration"""

    prometheus_url = os.getenv("PROMETHEUS_URL", "")
    prometheus_username = os.getenv("TELEMETRY_USERNAME", "")
    prometheus_password = os.getenv("TELEMETRY_PASSWORD", "")

    if not prometheus_password or not prometheus_url:
        return None

    # Convert URL to push gateway format
    if not prometheus_url.startswith("http"):
        prometheus_url = f"https://{prometheus_url}"

    try:
        metrics = PrometheusMetrics(
            gateway_url=prometheus_url.rstrip("/"),
            username=prometheus_username,
            password=prometheus_password,
            job_name="diceable-discord-bot",
        )
        return metrics
    except Exception:
        return None
