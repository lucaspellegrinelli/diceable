import logging
import os
from dataclasses import dataclass

import discord
import redis
from utils.suburb import SuburbWebsocket, setup_logger


@dataclass
class EnvVars:
    REDISHOST: str
    REDISPORT: int
    REDISUSER: str
    REDISPASSWORD: str
    DISCORD_TOKEN: str
    SUBURB_HOST: str
    SUBURB_TOKEN: str


@dataclass
class BotConfig:
    env: EnvVars
    logger: logging.Logger
    client: discord.Client
    tree: discord.app_commands.CommandTree
    redis_client: redis.Redis
    pubsub: SuburbWebsocket


def setup_config():
    def raise_error(var_name: str):
        raise ValueError(f"Environment variable {var_name} not set")

    env = EnvVars(
        REDISHOST=os.getenv("REDISHOST") or raise_error("REDISHOST"),
        REDISPORT=int(os.getenv("REDISPORT") or raise_error("REDISPORT")),
        REDISUSER=os.getenv("REDISUSER") or raise_error("REDISUSER"),
        REDISPASSWORD=os.getenv("REDISPASSWORD") or raise_error("REDISPASSWORD"),
        DISCORD_TOKEN=os.getenv("DISCORD_TOKEN") or raise_error("DISCORD_TOKEN"),
        SUBURB_HOST=os.getenv("SUBURB_HOST") or raise_error("SUBURB_HOST"),
        SUBURB_TOKEN=os.getenv("SUBURB_TOKEN") or raise_error("SUBURB_TOKEN"),
    )

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    return BotConfig(
        env=env,
        logger=setup_logger("diceable", "discord-py", env.SUBURB_HOST, env.SUBURB_TOKEN),
        client=client,
        tree=discord.app_commands.CommandTree(client),
        redis_client=redis.Redis(
            host=env.REDISHOST,
            port=env.REDISPORT,
            username=env.REDISUSER,
            password=env.REDISPASSWORD,
        ),
        pubsub=SuburbWebsocket(env.SUBURB_HOST, env.SUBURB_TOKEN),
    )
