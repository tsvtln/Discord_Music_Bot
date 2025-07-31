#!/usr/bin/python

from bin.main import BotRunner
from bin.events import EventHandlers
from bin.helpers import SuppressYouTubeMessages
import sys

# Create bot instance
bot = BotRunner()
client = bot.client

# Register event handlers
events = EventHandlers(bot)

# Run the bot
if __name__ == "__main__":
    sys.stdout = SuppressYouTubeMessages()
    client.run(bot.key)
