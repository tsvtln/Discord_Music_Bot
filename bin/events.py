"""
Event handlers for the Discord Music Bot
"""
import bin.db_helpers
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
import requests


class EventHandlers:
    def __init__(self, bot):
        self.bot = bot
        self.client = bot.client
        self.play_commands = PlayCommands(bot, bot.client)
        self.shell_handler = ShellCommandHandler(bot.client)
        self.lucky_draw_handler = LuckyDrawHandler(bot.client)
        self.weather_handler = WeatherCommandHandler(bot.client)
        self.keyword_worker = KeywordWorker(bot.client)
        self.scheduler_started = False  # Prevent multiple schedulers
        self.ansible_job_status = False  # Track if Ansible job status scheduler is running
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

    def send_ansible_job_status(self):
        if getattr(self, '_ansible_scheduler_started', False):
            return
        self._ansible_scheduler_started = True
        scheduler = AsyncIOScheduler()
        CHANNEL_ID = 1474763280970027070

        async def check_and_post_ansible_job():
            print('started')
            channel = self.client.get_channel(CHANNEL_ID)
            if not channel:
                print(f"Error: Channel {CHANNEL_ID} not found")
                return
            FINISH = False
            db_connector = bin.db_helpers.DBHelpers.get_conn()
            current_job_query = 'select job_id from job_id_tracker;'
            next_job = 'UPDATE job_id_tracker SET job_id = job_id + 1;'
            api_key = "select config_value from config where config_key='semaphore_api_key';"

            with db_connector.cursor() as cursor:
                cursor.execute(api_key)
                authorization_token = cursor.fetchone()[0]

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {authorization_token}"
            }

            while not FINISH:
                next_job_to_be_checked = 0
                job_output_build = []
                with db_connector.cursor() as cursor:
                    cursor.execute(current_job_query)
                    next_job_to_be_checked = int(cursor.fetchone()[0])

                url_raw_output = f"http://raspberrypi.local:3000/api/project/1/tasks/{next_job_to_be_checked}/raw_output"
                url_status = f"http://raspberrypi.local:3000/api/project/1/tasks/{next_job_to_be_checked}"
                try:
                    response = requests.get(url_raw_output, headers=headers)
                    job_status_summary = requests.get(url_status, headers=headers)
                except Exception as e:
                    print(e)
                    FINISH = True
                    continue
                if response.status_code != 200:
                    FINISH = True
                    continue
                else:
                    job_output = response.text.split('\n')
                    for index, item in enumerate(job_output):
                        if 'Run TaskRunner with template:' in item:
                            job_output_build.append((item.replace('Run TaskRunner with template: ', '')) + ' - ' +
                                                    job_status_summary.json()['status'])
                        elif 'Display upgraded packages summary' in item or 'Job Summary Output' in item:
                            if 'skipping' not in job_output[index + 1]:
                                index_start = index + 3
                                FINISH_OUTPUT = False
                                while not FINISH_OUTPUT:
                                    if 'TASK' in job_output[index_start] or 'PLAY RECAP' in job_output[index_start]:
                                        FINISH_OUTPUT = True
                                        continue
                                    job_output_build.append(job_output[index_start])
                                    index_start += 1
                    message = '\n'.join(job_output_build)
                    await channel.send(message)

                    with db_connector.cursor() as cursor:
                        cursor.execute(next_job)
                        db_connector.commit()

            db_connector.close()

        scheduler.add_job(check_and_post_ansible_job, CronTrigger(minute=0))
        scheduler.start()

    def register_events(self):
        """Register all event handlers"""
        self.client.event(self.on_voice_state_update)
        self.client.event(self.on_ready)
        self.client.event(self.on_message)

    async def on_voice_state_update(self, member, before, after):
        """Handle voice state updates - continue playing when users leave"""
        guild_id = member.guild.id
        # Check if bot is in voice and connected before trying to play
        if after.channel is None and self.bot.voice_clients.get(guild_id) is not None:
            voice_client = self.bot.voice_clients[guild_id]
            # Only continue if bot is connected and not playing but has songs queued
            if voice_client.is_connected() and not voice_client.is_playing() and self.bot.song_queues.get(guild_id):
                # Create a Player instance to handle the next song
                player = Player(guild_id, None, self.bot)
                await player.play_next_song()

    async def on_ready(self):  # verifies that the bot is started and sets a bot status
        print(f"Bot is ready")
        # Start daily maintenance scheduler
        try:
            from bin.maintenance_scheduler import start_scheduler
            start_scheduler()
        except Exception as e:
            print(f"Failed to start maintenance scheduler: {e}")
        self.start_fact_scheduler()
        self.send_ansible_job_status()
        self.client.loop.create_task(Presence.change_presence_periodically(self))
        await self.client.change_presence(activity=discord.Game(name=random.choice(VARS.presence_states)))

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
        if msg.content.startswith('$weather15'):
            await self.weather_handler.handle_weather_command(msg, 15)
            return

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
            await msg.channel.send(f"List of available commands:\n{'\n'.join(VARS.allowed_commands_list)}")

        # Output the list of commands
        if msg.content.startswith("$commands"):
            tp = '\n'.join(VARS.list_of_commands)
            await msg.channel.send(f"Куманди:\n{tp}")
