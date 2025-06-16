import discord
from utils.config import BotConfig
from utils.discord_roll import roll


class DiceButtonView(discord.ui.View):
    def __init__(self, config: BotConfig):
        super().__init__(timeout=60)
        self.config = config
        self.dice_amount = 1

    @discord.ui.select(
        placeholder="Choose number of dice",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label=f"{n} dice", value=n, default=n == 1)
            for n in range(1, 13)
        ],
    )
    async def select_dice_amount(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        self.dice_amount = int(select.values[0])
        await interaction.response.defer()

    @discord.ui.button(label="Roll D10", style=discord.ButtonStyle.primary, emoji="🎲")
    async def roll_d10_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        try:
            await interaction.message.delete()
        except:
            pass

        # Defer the interaction to avoid timeout
        await interaction.response.defer()

        # Now call roll with a followup interaction style
        await self._roll_with_followup(interaction, "d10", self.dice_amount, 0)

    @discord.ui.button(label="Roll D20", style=discord.ButtonStyle.primary, emoji="🎲")
    async def roll_d20_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        try:
            await interaction.message.delete()
        except:
            pass

        # Defer the interaction to avoid timeout
        await interaction.response.defer()

        # Now call roll with a followup interaction style
        await self._roll_with_followup(interaction, "d20", self.dice_amount, 0)

    async def _roll_with_followup(self, interaction, sides, amount, modifier):
        """Roll dice sending messages directly to channel to avoid interaction references"""
        import asyncio

        import discord
        from utils.discord_roll import (
            _generate_roll_message,
            _get_owner_id,
            _get_server_config,
            _roll_dice,
        )
        from utils.gif_generator import create_roll_gif

        server_id = str(interaction.guild_id)
        user_id = str(interaction.user.id)
        channel_id = str(interaction.channel_id)
        channel = interaction.channel

        owner_id = await _get_owner_id(self.config, server_id)

        if owner_id is None or not self.config.redis_client.hexists(
            "user-configs", owner_id
        ):
            return await channel.send(
                "```yaml\nServer not configured: No owner found```"
            )

        server_config = await _get_server_config(self.config, owner_id)

        if server_config is None:
            return await channel.send(
                "```yaml\nServer not configured: No config found```"
            )

        if not server_config.has_side(sides):
            return await channel.send(
                f"```yaml\nDice with {sides} sides not configured```"
            )

        dice_sides_config = server_config.get_side_config(sides)
        palette = dice_sides_config.get_player_palette(user_id)
        effect_name = dice_sides_config.get_player_effect(user_id)
        rolled_dice = _roll_dice(amount, sides)

        pub_content = {
            "server_id": server_id,
            "user_id": user_id,
            "channel_id": channel_id,
            "rolls": rolled_dice,
            "sides": sides,
            "palette": palette,
            "effect": effect_name,
        }

        self.config.websocket_publisher.publish_roll(owner_id, pub_content)
        self.config.logger.info(f"Rolling dice: {pub_content}")

        # Send initial rolling message directly to channel
        username = interaction.user.display_name or interaction.user.name
        rolling_msg = await channel.send(f"```yaml\n{username} rolls the dice...```")

        # Send GIF to channel
        await channel.send(
            content="",
            file=discord.File(
                create_roll_gif(
                    sides,
                    rolled_dice,
                    palette,
                    save_path="/app/data/roll_gifs",
                ),
                filename="roll.gif",
            ),
            delete_after=20,
        )

        await asyncio.sleep(4)

        # Delete the rolling message and send final results as new message
        try:
            await rolling_msg.delete()
        except:
            pass

        # Get username for the result
        username = interaction.user.display_name or interaction.user.name

        roll_str = _generate_roll_message(rolled_dice, modifier)
        await channel.send(f"```yaml\n{roll_str} -> {username}```")

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


def setup_roll_commands(config: BotConfig):
    @config.tree.command(name="roll", description="Roll dice")
    async def roll_command(interaction, amount: int, modifier: int = 0):
        await roll(interaction, config, "d10", amount, modifier)

    @config.tree.command(name="d10", description="Roll ten-sided dice")
    async def d10_command(interaction, amount: int, modifier: int = 0):
        await roll(interaction, config, "d10", amount, modifier)

    @config.tree.command(name="d20", description="Roll twenty-sided dice")
    async def d20_command(interaction, amount: int, modifier: int = 0):
        await roll(interaction, config, "d20", amount, modifier)

    @config.tree.command(
        name="dicebuttons", description="Show buttons to roll D10 or D20 dice"
    )
    async def dice_buttons_command(interaction):
        view = DiceButtonView(config)
        await interaction.response.send_message("", view=view)

    if not config.tree.get_command("roll"):
        config.tree.add_command(roll_command)

    if not config.tree.get_command("d10"):
        config.tree.add_command(d10_command)

    if not config.tree.get_command("d20"):
        config.tree.add_command(d20_command)

    if not config.tree.get_command("dicebuttons"):
        config.tree.add_command(dice_buttons_command)
