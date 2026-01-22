#!/usr/bin/python

"""
Discord Music Bot Runner
This script initializes and runs the Discord Music Bot.
It sets up the bot, registers event handlers, and starts the bot client.
"""


from bin.main import BotRunner
from bin.events import EventHandlers
from bin.helpers import SuppressYouTubeMessages
from libs.key_loaders import KeyLoader
import sys

# Create bot instance
debug = False
bot = BotRunner(debug)
client = bot.client

# Register event handlers
events = EventHandlers(bot)

# Run the bot
if __name__ == "__main__":
    sys.stdout = SuppressYouTubeMessages()  # Stops the spam from yt-dlp
    client.run(KeyLoader.bot_key())
