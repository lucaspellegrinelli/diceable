from utils.config import BotConfig
from utils.discord_roll import roll


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

    if not config.tree.get_command("roll"):
        config.tree.add_command(roll_command)

    if not config.tree.get_command("d10"):
        config.tree.add_command(d10_command)

    if not config.tree.get_command("d20"):
        config.tree.add_command(d20_command)
