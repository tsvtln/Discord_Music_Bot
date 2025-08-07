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
import random
from libs.global_vars import VARS
import discord
import os
import re
import datetime
import requests
from io import BytesIO
from PIL import Image, ImageSequence
import hashlib


class EventHandlers(BotRunner, VARS):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.client = bot.client
        self.play_commands = PlayCommands(bot, bot.client)
        self.shell_handler = ShellCommandHandler(bot.client)
        self.lucky_draw_handler = LuckyDrawHandler(bot.client)
        self.weather_handler = WeatherCommandHandler(bot.client)
        self.register_events()

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
        if msg.content.startswith('$kysmetche') or (msg.author == self.client.user and msg.content.strip().startswith('Ще срещнеш човек, който... АЗ ВИЖДАМ НУЛИТЕ И ЕДИНИЦИТЕ.')):
            await self.lucky_draw_handler.handle_lucky_draw(msg)
            return

        # Handle weather commands through the WeatherCommandHandler module
        if msg.content.startswith('$weather'):
            await self.weather_handler.handle_weather_command(msg)
            return

        keyword_gifs = {
            'наздраве': self.cheer,
            '1991': ['https://i.pinimg.com/736x/79/b7/84/79b784792d35c304af077ee2e450eea1.jpg'],
            'd1': self.d1,
        }

        keyword_strings = {}

        # Use string keys for gif_groups
        gif_groups = {
            'beer': self.beer_keywords,
            'kur': self.kur_keywords,
            'usl': self.usl_keywords,
            'its_wednesday': self.wednesday_keywords,
            'd1': self.d1_keywords,
        }

        # Loop through gif_groups to map keywords to GIF lists
        for gif_key, keywords in gif_groups.items():
            gif_list = getattr(self, gif_key)
            for word in keywords:
                keyword_gifs[word] = gif_list

        # Optimized group mapping for strings
        string_groups = {
            self.funny[0]: self.bot_keywords,
            self.funny[1]: self.haralampi_keywords,
        }

        # Loop through string_groups to map keywords to string responses
        for string_value, keywords in string_groups.items():
            for word in keywords:
                keyword_strings[word] = string_value

        lowered = msg.content.lower()

        # First, check for string responses
        for word, response in keyword_strings.items():
            if re.search(rf'\b{re.escape(word)}\b', lowered):
                await msg.channel.send(response)
                return

        # Only check for wednesday keywords and respond accordingly if matched
        if any(re.search(rf'\b{re.escape(word)}\b', lowered) for word in self.wednesday_keywords):
            today = datetime.datetime.now().strftime('%A')
            if today.lower() == 'wednesday':
                gif_list = self.its_wednesday
            else:
                gif_list = self.not_wednesday
            gif_url = random.choice(gif_list)
            cache_dir = 'cache/gif_cache'
            os.makedirs(cache_dir, exist_ok=True)
            url_hash = hashlib.md5(gif_url.encode('utf-8')).hexdigest()
            cache_path = os.path.join(cache_dir, f'wednesday_{url_hash}.gif')
            if os.path.exists(cache_path):
                await msg.channel.send(file=discord.File(fp=cache_path, filename='wednesday.gif'))
            else:
                try:
                    response = requests.get(gif_url)
                    response.raise_for_status()
                    original_gif = Image.open(BytesIO(response.content))
                    frames = []
                    for frame in ImageSequence.Iterator(original_gif):
                        frame = frame.convert('RGBA')
                        frame = frame.resize((120, 120), resample=Image.Resampling.LANCZOS)
                        frame = frame.convert('P', palette=Image.Palette.ADAPTIVE, dither=Image.Dither.FLOYDSTEINBERG)
                        frames.append(frame)
                    frames[0].save(cache_path, format='GIF', save_all=True, append_images=frames[1:], loop=0, duration=original_gif.info.get('duration', 40), disposal=2, transparency=original_gif.info.get('transparency', 0))
                    await msg.channel.send(file=discord.File(fp=cache_path, filename='wednesday.gif'))
                except Exception as e:
                    print(e)
                    await msg.channel.send(gif_url)
            return

        # Then, check for GIF responses
        for word, gif_list in keyword_gifs.items():
            if re.search(rf'\b{re.escape(word)}\b', lowered):
                gif_url = random.choice(gif_list)
                cache_dir = 'cache/gif_cache'
                os.makedirs(cache_dir, exist_ok=True)
                url_hash = hashlib.md5(gif_url.encode('utf-8')).hexdigest()
                cache_path = os.path.join(cache_dir, f'{word}_{url_hash}.gif')
                if os.path.exists(cache_path):
                    await msg.channel.send(file=discord.File(fp=cache_path, filename=f'{word}.gif'))
                else:
                    try:
                        response = requests.get(gif_url)
                        response.raise_for_status()
                        original_gif = Image.open(BytesIO(response.content))
                        frames = []
                        for frame in ImageSequence.Iterator(original_gif):
                            frame = frame.convert('RGBA')
                            frame = frame.resize((120, 120), resample=Image.Resampling.LANCZOS)
                            frame = frame.convert('P', palette=Image.Palette.ADAPTIVE,
                                                  dither=Image.Dither.FLOYDSTEINBERG)
                            frames.append(frame)
                        frames[0].save(cache_path, format='GIF', save_all=True, append_images=frames[1:], loop=0, duration=original_gif.info.get('duration', 40), disposal=2, transparency=original_gif.info.get('transparency', 0))
                        await msg.channel.send(file=discord.File(fp=cache_path, filename=f'{word}.gif'))
                    except Exception as e:
                        print(f"GIF processing error for {word}: {e}")
                        await msg.channel.send(gif_url)
                return

        # Other Commands
        if msg.content.startswith("$key_words"):
            all_keywords = set(
                self.beer_keywords +
                self.kur_keywords +
                self.usl_keywords +
                self.bot_keywords +
                self.haralampi_keywords +
                self.wednesday_keywords +
                list(keyword_gifs.keys())
            )
            await msg.channel.send(f"Ключови думи:\n{', '.join(sorted(all_keywords))}")

        if msg.content.startswith("$cmds"):
            await msg.channel.send(f"List of available commands:\n{'\n'.join(self.allowed_commands_list)}")

        # Output the list of commands
        if msg.content.startswith("$commands"):
            tp = '\n'.join(self.list_of_commands)
            await msg.channel.send(f"Куманди:\n{tp}")
