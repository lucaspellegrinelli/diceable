import asyncio
from collections.abc import Awaitable as ABCAwaitable
import json
import logging
import random
from typing import Literal

import discord

from models.server import parse_discord_server_config

from .config import BotConfig
from .gif_generator import create_roll_gif


def _roll_dice(
    amount: int,
    sides: Literal["d10"] | Literal["d20"],
):
    max_dice_result = 10 if sides == "d10" else 20
    rolled_dice = [random.randint(1, max_dice_result) for _ in range(amount)]
    return sorted(rolled_dice, key=lambda x: x if x > 0 else 999)


def _generate_roll_message(rolled_dice, modifier):
    modifier_sign = "+" if modifier >= 0 else "-"
    modifier_str = f" {modifier_sign}{abs(modifier)}" if modifier != 0 else ""
    result_str = ", ".join([str(die + modifier) for die in rolled_dice])
    return f"Resultados: [{result_str}]{modifier_str}"


async def _get_owner_id(config: BotConfig, server_id: str):
    if not config.redis_client.hexists("user-servers", server_id):
        return None

    owner_id = config.redis_client.hget("user-servers", server_id)

    if isinstance(owner_id, ABCAwaitable):
        owner_id = await owner_id

    return owner_id


async def _get_server_config(config: BotConfig, owner_id: str):
    if owner_id is None or not config.redis_client.hexists(
        "user-configs", owner_id
    ):
        return None

    server_config = config.redis_client.hget("user-configs", owner_id)

    if isinstance(server_config, ABCAwaitable):
        server_config = await server_config

    if server_config is None:
        return None

    json_config = json.loads(server_config)
    return parse_discord_server_config(json_config)


async def roll(
    interaction,
    config: BotConfig,
    sides: Literal["d10"] | Literal["d20"],
    amount: int,
    modifier: int = 0,
):
    server_id = str(interaction.guild_id)
    user_id = str(interaction.user.id)
    channel_id = str(interaction.channel_id)

    owner_id = await _get_owner_id(config, server_id)

    if owner_id is None or not config.redis_client.hexists(
        "user-configs", owner_id
    ):
        return await interaction.response.send_message(
            "```yaml\nServer not configured```",
        )

    server_config = await _get_server_config(config, owner_id)

    if server_config is None:
        return await interaction.response.send_message(
            "```yaml\nServer not configured```",
        )

    if not server_config.has_side(sides):
        return await interaction.response.send_message(
            "```yaml\nDice not configured. Contact an admin.```",
        )

    dice_sides_config = server_config.get_side_config(sides)
    palette = dice_sides_config.get_player_palette(user_id)
    effect_name = dice_sides_config.get_player_effect(user_id)
    rolled_dice = _roll_dice(amount, sides)

    pub_content = {
        "server_id": server_id,
        "user_id": owner_id,
        "channel_id": channel_id,
        "rolls": rolled_dice,
        "sides": sides,
        "palette": palette,
        "effect": effect_name,
    }

    config.sio.emit("roll", pub_content)
    config.logger.log(logging.INFO, f"Rolling dice: {pub_content}")

    await interaction.response.send_message(
        "```yaml\nRolling dice...```",
    )

    channel = interaction.channel
    await channel.send(
        content="",
        file=discord.File(
            create_roll_gif(sides, rolled_dice, palette),
            filename="roll.gif"
        ),
        delete_after=20
    )

    orig_response = await interaction.original_response()
    await asyncio.sleep(4)

    roll_str = _generate_roll_message(rolled_dice, modifier)
    await orig_response.edit(content=f"```yaml\n{roll_str}```")
