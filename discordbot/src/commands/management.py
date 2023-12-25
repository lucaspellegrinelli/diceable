from collections.abc import Awaitable as ABCAwaitable
from models.server import DiscordServerConfig

from utils.config import BotConfig


def setup_management_commands(config: BotConfig):
    @config.tree.command(name="register", description="Register server")
    async def register_command(interaction):
        server_id = str(interaction.guild_id)
        user_id = str(interaction.user.id)

        if config.redis_client.hexists("user-servers", server_id):
            return await interaction.response.send_message(
                "```yaml\nServer already registered```"
            )

        config.redis_client.hset("user-servers", server_id, user_id)

        if not config.redis_client.hexists("user-configs", user_id):
            config.redis_client.hset(
                "user-configs",
                user_id,
                DiscordServerConfig.default().to_json()
            )

        return await interaction.response.send_message(
            f"```yaml\nServer registered to {user_id}```"
        )

    @config.tree.command(name="unregister", description="Unregister server")
    async def unregister_command(interaction):
        server_id = str(interaction.guild_id)
        user_id = str(interaction.user.id)

        if not config.redis_client.hexists("user-servers", server_id):
            return await interaction.response.send_message(
                "```yaml\nServer not registered```"
            )

        owner_id = config.redis_client.hget("user-servers", server_id)

        if isinstance(owner_id, ABCAwaitable):
            owner_id = await owner_id

        if owner_id is None:
            return await interaction.response.send_message(
                "```yaml\nServer not configured```"
            )

        if owner_id != user_id:
            return await interaction.response.send_message(
                "```yaml\nYou are not the owner of this server```"
            )

        config.redis_client.hdel("user-servers", [server_id])
        await interaction.response.send_message(
            "```yaml\nServer unregistered```"
        )

    if not config.tree.get_command("register"):
        config.tree.add_command(register_command)

    if not config.tree.get_command("unregister"):
        config.tree.add_command(unregister_command)
