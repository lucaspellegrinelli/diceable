import logging
import signal
import sys
import time

from dotenv import load_dotenv

from commands.management import setup_management_commands
from commands.roll import setup_roll_commands
from utils.config import setup_config


load_dotenv()
config = setup_config()


@config.client.event
async def on_ready():
    setup_roll_commands(config)
    setup_management_commands(config)

    await config.tree.sync()
    config.logger.log(logging.INFO, f"Logged in as {config.client.user}")


@config.sio.event
def connect():
    config.logger.log(logging.INFO, "Connected to socket.io")


@config.sio.event
def disconnect():
    config.logger.log(logging.INFO, "Disconnected from socket.io")


def signal_handler(sig, _):
    config.logger.log(logging.INFO, f"Received signal {sig}. Exiting...")
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


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
