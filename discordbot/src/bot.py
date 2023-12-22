import logging
import time
from dotenv import load_dotenv

from utils.config import setup_config
from commands.roll import setup_roll_commands
from commands.management import setup_management_commands


# Setup config
load_dotenv()
config = setup_config()

# Setup commands
setup_roll_commands(config)
setup_management_commands(config)


@ config.client.event
async def on_ready():
    await config.tree.sync()
    config.logger.log(logging.INFO, f"Logged in as {config.client.user}")


@ config.sio.event
def connect():
    config.logger.log(logging.INFO, "Connected to socket.io")


@ config.sio.event
def disconnect():
    config.logger.log(logging.INFO, "Disconnected from socket.io")


if __name__ == "__main__":
    while True:
        try:
            config.sio.connect(config.env.SOCKETIO_URL)
            break
        except Exception:
            config.logger.log(
                logging.INFO, "Socket.io connection error. Retrying in 5s..."
            )
            time.sleep(5)

    config.client.run(config.env.DISCORD_TOKEN)
