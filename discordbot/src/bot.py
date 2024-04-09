import logging
import signal
import sys

from commands.management import setup_management_commands
from commands.roll import setup_roll_commands
from dotenv import load_dotenv
from utils.config import setup_config

load_dotenv()
config = setup_config()
config.logger.setLevel(logging.INFO)


@config.client.event
async def on_ready():
    setup_roll_commands(config)
    setup_management_commands(config)

    await config.tree.sync()
    config.logger.info(f"Logged in as {config.client.user}")


@config.sio.event
def connect():
    config.logger.info("Connected to socket.io.")


@config.sio.event
def disconnect():
    config.logger.info("Disconnected from socket.io.")


def signal_handler(sig, _):
    config.logger.info(f"Received signal {sig}. Exiting...")
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    # try:
    #     config.sio.connect(config.env.SOCKETIO_URL)
    # except Exception as error:
    #     config.logger.error(f"Failed to connect to socket.io: {error}")

    config.client.run(config.env.DISCORD_TOKEN)
