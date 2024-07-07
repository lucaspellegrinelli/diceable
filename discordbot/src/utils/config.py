import logging
import os
from dataclasses import dataclass

import discord
import redis
import socketio


@dataclass
class EnvVars:
    REDISHOST: str
    REDISPORT: int
    REDISUSER: str
    REDISPASSWORD: str
    DISCORD_TOKEN: str
    SOCKETIO_URL: str


@dataclass
class BotConfig:
    env: EnvVars
    logger: logging.Logger
    client: discord.Client
    tree: discord.app_commands.CommandTree
    redis_client: redis.Redis
    sio: socketio.Client


def setup_config():
    def raise_error(var_name: str):
        raise ValueError(f"Environment variable {var_name} not set")

    env = EnvVars(
        REDISHOST=os.getenv("REDISHOST") or raise_error("REDISHOST"),
        REDISPORT=int(os.getenv("REDISPORT") or raise_error("REDISPORT")),
        REDISUSER=os.getenv("REDISUSER") or raise_error("REDISUSER"),
        REDISPASSWORD=os.getenv("REDISPASSWORD") or raise_error("REDISPASSWORD"),
        DISCORD_TOKEN=os.getenv("DISCORD_TOKEN") or raise_error("DISCORD_TOKEN"),
        SOCKETIO_URL=os.getenv("SOCKETIO_URL") or raise_error("SOCKETIO_URL"),
    )

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    return BotConfig(
        env=env,
        logger=logging.getLogger("discord"),
        client=client,
        tree=discord.app_commands.CommandTree(client),
        redis_client=redis.Redis(
            host=env.REDISHOST,
            port=env.REDISPORT,
            username=env.REDISUSER,
            password=env.REDISPASSWORD,
        ),
        sio=socketio.Client(),
    )
