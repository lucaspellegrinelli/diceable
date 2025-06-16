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
        await interaction.message.delete()
        await interaction.response.defer()
        await roll(
            interaction, self.config, "d10", self.dice_amount, 0, as_response=False
        )

    @discord.ui.button(label="Roll D20", style=discord.ButtonStyle.primary, emoji="🎲")
    async def roll_d20_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.message.delete()
        await interaction.response.defer()
        await roll(
            interaction, self.config, "d20", self.dice_amount, 0, as_response=False
        )

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
