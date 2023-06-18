import asyncio
import json
import logging
import os
import random

import discord
import redis
from discord import app_commands
from dotenv import load_dotenv
from src.cloudflare import get_dice_cdn_urls
from src.gifgenerator import create_roll_gif

load_dotenv()

logger = logging.getLogger("discord")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

DEFAULT_PALETTE = [
    "red",
    "green",
    "blue",
    "blue",
    "blue",
    "blue",
    "blue",
    "blue",
    "blue",
    "blue",
]

DEFAULT_CONFIG = {
    "custom_colors": "false",
    "palettes": {},  # { "PALETTE_NAME": ["color", "color", ...] }
    "player_skins": {},  # { "DISCORD_ID": { "palette": None, "effect": None } }
}

redis_client = None
dice_cdn_urls = None


def _generate_roll_message(rolled_dice, modifier):
    modifier_sign = "+" if modifier >= 0 else "-"
    modifier_str = f" {modifier_sign}{abs(modifier)}" if modifier != 0 else ""
    result_str = ", ".join([str(die + modifier) for die in rolled_dice])
    return f"Resultados: [{result_str}]{modifier_str}"


def _repond_interaction(interaction, message, **kwargs):
    return interaction.response.send_message(f"```yaml\n{message}```", **kwargs)


@tree.command(name="roll", description="Roll dice")
async def roll_command(interaction, amount: int, modifier: int = 0):
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

    player_skin = server_config["player_skins"].get(user_id, {})
    palette_name = player_skin.get("palette", None)
    effect_name = player_skin.get("effect", None)
    palette = server_config["palettes"].get(palette_name, DEFAULT_PALETTE)

    rolled_dice = [random.randint(1, 10) for _ in range(amount)]
    rolled_dice = sorted(rolled_dice, key=lambda x: x if x > 0 else 999)

    pub_content = {
        "server_id": server_id,
        "user_id": user_id,
        "channel_id": channel_id,
        "rolls": rolled_dice,
        "palette": palette,
        "effect": effect_name,
    }

    redis_client.publish("rolls", json.dumps(pub_content))
    await _repond_interaction(interaction, "Rolling dice...")

    gif_path = create_roll_gif(rolled_dice, palette, 16, dice_cdn_urls, "rolls")
    roll_str = _generate_roll_message(rolled_dice, modifier)

    channel = interaction.channel
    await channel.send(
        "", file=discord.File(gif_path, filename="roll.gif"), delete_after=20
    )
    orig_response = await interaction.original_response()
    await asyncio.sleep(4)
    await orig_response.edit(content=f"```yaml\n{roll_str}```")


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


if __name__ == "__main__":
    load_dotenv()

    dice_cdn_urls = get_dice_cdn_urls(
        cloudflare_account_id=os.getenv("CLOUDFLARE_ACCOUNT_ID"),
        cloudflare_assets_api_token=os.getenv("CLOUDFLARE_ASSETS_API_TOKEN"),
    )

    redis_client = redis.Redis(
        host=os.getenv("REDISHOST"),
        port=int(os.getenv("REDISPORT")),
        username=os.getenv("REDISUSER"),
        password=os.getenv("REDISPASSWORD"),
    )

    client.run(os.getenv("DISCORD_TOKEN"))
