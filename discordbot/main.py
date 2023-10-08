import asyncio
import json
import logging
import os
import time
import random
from typing import Literal

import discord
import redis
import socketio
from discord import app_commands
from dotenv import load_dotenv
from src.gifgenerator import create_roll_gif

load_dotenv()

logger = logging.getLogger("discord")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

sio = socketio.Client()

redis_client = None


def _generate_roll_message(rolled_dice, modifier):
    modifier_sign = "+" if modifier >= 0 else "-"
    modifier_str = f" {modifier_sign}{abs(modifier)}" if modifier != 0 else ""
    result_str = ", ".join([str(die + modifier) for die in rolled_dice])
    return f"Resultados: [{result_str}]{modifier_str}"


def _repond_interaction(interaction, message, **kwargs):
    return interaction.response.send_message(f"```yaml\n{message}```", **kwargs)


async def roll(
    interaction, sides: Literal["d10"] | Literal["d20"], amount: int, modifier: int = 0
):
    server_id = str(interaction.guild_id)
    user_id = str(interaction.user.id)
    channel_id = str(interaction.channel_id)

    if not redis_client.hexists("user-servers", server_id):
        return await _repond_interaction(interaction, "Server not registered")

    owner_id = redis_client.hget("user-servers", server_id)
    if owner_id is None or not redis_client.hexists("user-configs", owner_id):
        return await _repond_interaction(interaction, "Server not configured")

    server_config = redis_client.hget("user-configs", owner_id)
    if server_config is None:
        return await _repond_interaction(interaction, "Server not configured")

    server_config = json.loads(server_config)
    if not sides in server_config:
        return await _repond_interaction(
            interaction, "Dice not configured. Contact an admin."
        )

    dice_sides_config = server_config.get(sides, {})

    custom_colors = dice_sides_config.get("custom_colors") == "true"
    default_palette = dice_sides_config.get("default_palette", None)
    player_skin = dice_sides_config["player_skins"].get(user_id, {})
    palette_name = player_skin.get("palette", None)
    effect_name = player_skin.get("effect", None)

    palette = dice_sides_config["palettes"].get(default_palette)
    if custom_colors:
        palette = dice_sides_config["palettes"].get(palette_name, palette)

    max_dice_result = 10 if sides == "d10" else 20
    rolled_dice = [random.randint(1, max_dice_result) for _ in range(amount)]
    rolled_dice = sorted(rolled_dice, key=lambda x: x if x > 0 else 999)

    pub_content = {
        "server_id": server_id,
        "user_id": owner_id.decode("utf-8"),
        "channel_id": channel_id,
        "rolls": rolled_dice,
        "sides": sides,
        "palette": palette,
        "effect": effect_name,
    }

    sio.emit("roll", pub_content)
    logger.log(logging.INFO, f"Rolling dice: {pub_content}")

    await _repond_interaction(interaction, "Rolling dice...")

    gif_path = create_roll_gif(sides, rolled_dice, palette, 12, "rolls")
    roll_str = _generate_roll_message(rolled_dice, modifier)

    channel = interaction.channel
    await channel.send(
        "", file=discord.File(gif_path, filename="roll.gif"), delete_after=20
    )
    orig_response = await interaction.original_response()
    await asyncio.sleep(4)
    await orig_response.edit(content=f"```yaml\n{roll_str}```")


@tree.command(name="roll", description="Roll dice")
async def roll_command(interaction, amount: int, modifier: int = 0):
    await roll(interaction, "d10", amount, modifier)


@tree.command(name="d10", description="Roll ten-sided dice")
async def d10_command(interaction, amount: int, modifier: int = 0):
    await roll(interaction, "d10", amount, modifier)


@tree.command(name="d20", description="Roll twenty-sided dice")
async def d20_command(interaction, amount: int, modifier: int = 0):
    await roll(interaction, "d20", amount, modifier)


@tree.command(name="register", description="Register server")
async def register_command(interaction):
    server_id = interaction.guild_id
    user_id = interaction.user.id

    if redis_client.hexists("user-servers", server_id):
        return await _repond_interaction(interaction, "Server already registered")

    redis_client.hset("user-servers", server_id, user_id)
    return await _repond_interaction(interaction, f"Server registered to {user_id}")


@tree.command(name="unregister", description="Unregister server")
async def unregister_command(interaction):
    server_id = interaction.guild_id
    user_id = interaction.user.id

    if not redis_client.hexists("user-servers", server_id):
        return await _repond_interaction(interaction, "Server not registered")

    owner_id = redis_client.hget("user-servers", server_id)
    if owner_id is None:
        return await _repond_interaction(interaction, "Server not configured")

    owner_id = int(owner_id.decode("utf-8"))
    if owner_id != user_id:
        return await _repond_interaction(
            interaction, "You are not the owner of this server"
        )

    redis_client.hdel("user-servers", server_id)
    return await _repond_interaction(interaction, "Server unregistered")


@client.event
async def on_ready():
    await tree.sync()
    logger.log(logging.INFO, f"Logged in as {client.user}")


@sio.event
def connect():
    logger.log(logging.INFO, "Connected to socket.io")


@sio.event
def disconnect():
    logger.log(logging.INFO, "Disconnected to socket.io")


if __name__ == "__main__":
    load_dotenv()

    while True:
        try:
            sio.connect(os.getenv("SOCKETIO_URL"))
            break
        except socketio.exceptions.ConnectionError:
            logger.log(logging.INFO, "Socket.io connection error. Retrying in 5s...")
            time.sleep(5)

    redis_client = redis.Redis(
        host=os.getenv("REDISHOST"),
        port=int(os.getenv("REDISPORT")),
        username=os.getenv("REDISUSER"),
        password=os.getenv("REDISPASSWORD"),
    )

    client.run(os.getenv("DISCORD_TOKEN"))
