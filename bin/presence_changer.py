"""
All this module does is change the bot's presence periodically.
It uses the `discord.py` library to set a random status from a predefined list every 30 minutes.
"""

import discord
import asyncio
import random
from .main import BotRunner


class Presence(BotRunner):
    def __init__(self, client):
        super().__init__()
        self.client = client

    async def change_presence_periodically(self):
        while True:
            await self.client.change_presence(activity=discord.Game(name=random.choice(self.presence_states)))
            await asyncio.sleep(1800)  # 30 minutes
