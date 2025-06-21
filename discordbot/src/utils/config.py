import logging
import os
from dataclasses import dataclass
from typing import Optional

import discord
import redis
from utils.dice_websocket import DiceWebSocketPublisher
from utils.loki_logger import setup_loki_logger
from utils.prometheus_metrics import PrometheusMetrics, setup_prometheus_metrics


@dataclass
class EnvVars:
    REDISHOST: str
    REDISPORT: int
    REDISUSER: str
    REDISPASSWORD: str
    DISCORD_TOKEN: str
    WEBSOCKET_HOST: str


@dataclass
class BotConfig:
    env: EnvVars
    logger: logging.Logger
    client: discord.Client
    tree: discord.app_commands.CommandTree
    redis_client: redis.Redis
    websocket_publisher: DiceWebSocketPublisher
    metrics: Optional[PrometheusMetrics]


def setup_config():
    def raise_error(var_name: str):
        raise ValueError(f"Environment variable {var_name} not set")

    env = EnvVars(
        REDISHOST=os.getenv("REDISHOST") or raise_error("REDISHOST"),
        REDISPORT=int(os.getenv("REDISPORT") or raise_error("REDISPORT")),
        REDISUSER=os.getenv("REDISUSER") or raise_error("REDISUSER"),
        REDISPASSWORD=os.getenv("REDISPASSWORD") or raise_error("REDISPASSWORD"),
        DISCORD_TOKEN=os.getenv("DISCORD_TOKEN") or raise_error("DISCORD_TOKEN"),
        WEBSOCKET_HOST=os.getenv("WEBSOCKET_HOST") or raise_error("WEBSOCKET_HOST"),
    )

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    # Setup Prometheus metrics
    metrics = setup_prometheus_metrics()
    logger = setup_loki_logger()

    if metrics:
        logger.info("Prometheus metrics initialized")
    else:
        logger.warning(
            "Prometheus metrics not configured - missing PROMETHEUS_URL or TELEMETRY_PASSWORD"
        )

    return BotConfig(
        env=env,
        logger=logger,
        client=client,
        tree=discord.app_commands.CommandTree(client),
        redis_client=redis.Redis(
            host=env.REDISHOST,
            port=env.REDISPORT,
            username=env.REDISUSER,
            password=env.REDISPASSWORD,
        ),
        websocket_publisher=DiceWebSocketPublisher(env.WEBSOCKET_HOST),
        metrics=metrics,
    )
