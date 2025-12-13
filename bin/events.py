"""
Event handlers for the Discord Music Bot
"""
from .main import BotRunner
from .player import Player
from .presence_changer import Presence
from .on_message.play_commands import PlayCommands
from .on_message.handle_shell_cmds import ShellCommandHandler
from .on_message.lucky_draw import LuckyDrawHandler
from .on_message.weather_cmd import WeatherCommandHandler
from .on_message.keyword_worker import KeywordWorker
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from libs.daily_fact import get_today_fact
import random
from libs.global_vars import VARS
import discord


class EventHandlers(BotRunner, VARS):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.client = bot.client
        self.play_commands = PlayCommands(bot, bot.client)
        self.shell_handler = ShellCommandHandler(bot.client)
        self.lucky_draw_handler = LuckyDrawHandler(bot.client)
        self.weather_handler = WeatherCommandHandler(bot.client)
        self.keyword_worker = KeywordWorker(bot.client)
        self.scheduler_started = False  # Prevent multiple schedulers
        self.register_events()

    def start_fact_scheduler(self):
        if getattr(self, '_fact_scheduler_started', False):
            return
        self._fact_scheduler_started = True
        scheduler = AsyncIOScheduler()
        # channel ids to post the daily fact to
        CHANNEL_IDS = [305337312705904642, 1403142694317981836]

        async def post_daily_fact():
            fact = get_today_fact()
            for c in CHANNEL_IDS:
                channel = self.client.get_channel(c)
                if channel:
                    await channel.send(f"🧠 Daily Fact: {fact}")
        scheduler.add_job(post_daily_fact, CronTrigger(hour=16, minute=20))
        scheduler.start()

    def register_events(self):
        """Register all event handlers"""
        self.client.event(self.on_voice_state_update)
        self.client.event(self.on_ready)
        self.client.event(self.on_message)

    async def on_voice_state_update(self, member, before, after):
        """Handle voice state updates - continue playing when users leave"""
        guild_id = member.guild.id
        if after.channel is None and self.bot.voice_clients.get(guild_id) is not None:
            if not self.bot.voice_clients[guild_id].is_playing() and self.bot.song_queues.get(guild_id):
                # Create a Player instance to handle the next song
                player = Player(guild_id, None, self.bot)
                await player.play_next_song()

    async def on_ready(self):  # verifies that the bot is started and sets a bot status
        print(f"Bot is ready")
        self.start_fact_scheduler()
        self.client.loop.create_task(Presence.change_presence_periodically(self))
        await self.client.change_presence(activity=discord.Game(name=random.choice(self.presence_states)))

    async def on_message(self, msg):
        """Main message handler for all bot functionality"""
        # Handle shell commands through the ShellCommandHandler module
        await self.shell_handler.handle_shell_command(msg)

        # Handle music commands through the PlayCommands module
        if msg.content.startswith(('$play', '$pause', '$resume', '$stop', '$queue')):
            await self.play_commands.handle_music_commands(msg)
            return

        # Handle lucky draw commands through the LuckyDrawHandler module
        if (msg.content.startswith('$kysmetche') or
                (
                        msg.author == self.client.user and
                        msg.content.strip().startswith('Ще срещнеш човек, който... АЗ ВИЖДАМ НУЛИТЕ И ЕДИНИЦИТЕ.'))):
            await self.lucky_draw_handler.handle_lucky_draw(msg)
            return

        # Handle weather commands through the WeatherCommandHandler module
        if msg.content.startswith('$weather5'):
            await self.weather_handler.handle_weather_command(msg, 5)
            return

        if msg.content.startswith('$weather'):
            await self.weather_handler.handle_weather_command(msg, 1)
            return

        # Handle keyword-related commands
        if await self.keyword_worker.handle_keyword_commands(msg):
            return

        # Handle keyword responses (GIFs and strings)
        if await self.keyword_worker.handle_keyword_responses(msg):
            return

        # Other Commands
        if msg.content.startswith("$cmds"):
            await msg.channel.send(f"List of available commands:\n{'\n'.join(self.allowed_commands_list)}")

        # Output the list of commands
        if msg.content.startswith("$commands"):
            tp = '\n'.join(self.list_of_commands)
            await msg.channel.send(f"Куманди:\n{tp}")
