import asyncio
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


@ config.client.event
async def on_ready():
    setup_roll_commands(config)
    setup_management_commands(config)

    await config.tree.sync()
    config.logger.log(logging.INFO, f"Logged in as {config.client.user}")


@ config.sio.event
def connect():
    config.logger.log(logging.INFO, "Connected to socket.io")


@ config.sio.event
def disconnect():
    config.logger.log(logging.INFO, "Disconnected from socket.io")


async def close_and_disconnect_services():
    await config.client.close()
    config.sio.disconnect()


def signal_handler(sig, _):
    config.logger.log(logging.INFO, f"Received signal {sig}. Exiting...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(close_and_disconnect_services())
    loop.close()
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
