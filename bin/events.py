"""
Event handlers for the Discord Music Bot
"""
from .main import BotRunner
from .player import Player
from .presence_changer import Presence
import random
from libs.global_vars import VARS
import discord


class EventHandlers(BotRunner, VARS):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.client = bot.client
        self.register_events()

    def register_events(self):
        """Register all event handlers"""
        self.client.event(self.on_voice_state_update)
        self.client.event(self.on_ready)
        # Add more event handlers here as needed
        # self.client.event(self.on_message)
        # self.client.event(self.on_ready)

    async def on_voice_state_update(self, member, before, after):
        """Handle voice state updates - continue playing when users leave"""
        guild_id = member.guild.id
        if after.channel is None and self.bot.voice_clients.get(guild_id) is not None:
            if not self.bot.voice_clients[guild_id].is_playing() and self.bot.song_queues.get(guild_id):
                # Create a Player instance to handle the next song
                player = Player(guild_id, None)
                await player.play_next_song()

    async def on_ready(self):  # verifies that the bot is started and sets a bot status
        print(f"Bot is ready")
        self.client.loop.create_task(Presence.change_presence_periodically(self))
        await self.client.change_presence(activity=discord.Game(name=random.choice(self.presence_states)))
