"""
Music playback commands module for the Discord Music Bot
Handles all music-related commands: play, pause, resume, stop, queue
"""

import asyncio
import yt_dlp
from collections import deque
import functools
from ..player import Player
from libs.global_vars import VARS


class PlayCommands(VARS):
    def __init__(self, bot, client):
        super().__init__()
        self.bot = bot
        self.client = client

    async def handle_music_commands(self, msg):
        """Handle all music-related commands"""
        # Music playback commands
        if msg.content.startswith('$play'):
            await self.handle_play_command(msg)

        # Player Control Commands
        if msg.content.startswith("$pause"):
            try:
                self.bot.voice_clients[msg.guild.id].pause()
            except Exception as err:
                print(err)

        if msg.content.startswith("$resume"):
            try:
                self.bot.voice_clients[msg.guild.id].resume()
            except Exception as err:
                print(err)

        if msg.content.startswith("$stop"):
            try:
                self.bot.voice_clients[msg.guild.id].stop()
                await self.bot.voice_clients[msg.guild.id].disconnect()
                if msg.guild.id in self.bot.song_queues:
                    del self.bot.song_queues[msg.guild.id]
                self.bot.song_queue_name.clear()
            except Exception as err:
                print(err)

        if msg.content.startswith("$queue"):
            if msg.guild.id in self.bot.song_queues and self.bot.song_queue_name:
                formatted_queue = [f"{i}. {name}" for i, name in enumerate(self.bot.song_queue_name, 1)]
                queue_list = '\n'.join(formatted_queue)
                await msg.channel.send(f"Плейлист:\n{queue_list}")
            else:
                await msg.channel.send('Нема плейлист')

    async def handle_play_command(self, msg):
        """Handle music playback command"""
        if msg.guild.id not in self.bot.voice_clients:
            try:
                voice_channel = msg.author.voice.channel
                voice_client = await voice_channel.connect()
                self.bot.voice_clients[voice_client.guild.id] = voice_client
            except Exception as err:
                await msg.channel.send('Влез във voice канал, иначе тре серенада пред блока ти праа.')
                print(err)
                return

        try:
            test_for_url = msg.content.split()
            if len(test_for_url) > 1:
                test_for_url = deque(test_for_url[1:])
                url = ' '.join(test_for_url)
            else:
                url = test_for_url[1]

            if url == 'skakauec':
                url = 'https://www.youtube.com/watch?v=pq3C-UE6RE0'
            elif url == 'sans':
                url = 'https://www.youtube.com/watch?v=0FCvzsVlXpQ'
            elif url == 'ignf':
                url = 'https://www.youtube.com/watch?v=yLnd3AYEd2k'
            elif 'http' not in url:
                from ..helpers import Helpers
                url = await Helpers.find_video_url(url)

            if msg.guild.id not in self.bot.song_queues:
                self.bot.song_queues[msg.guild.id] = []

            # Extract info once
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, functools.partial(self.bot.ytdl.extract_info, url, download=False))
            video_name = info.get('title', 'Video title not available')
            audio_url = info['url']

            if video_name != 'Video title not available':
                await msg.channel.send(f"Добавена песен в плейлиста: {video_name}")
                self.bot.song_queues[msg.guild.id].append((url, video_name, audio_url))
                self.bot.song_queue_name.append(video_name)
            else:
                await msg.channel.send('Пробуем при намирането на таз песен.')

            if len(self.bot.song_queues[msg.guild.id]) == 1 and not self.bot.voice_clients[msg.guild.id].is_playing():
                player = Player(msg.guild.id, msg, self.bot)
                await player.play_next_song()

        except yt_dlp.DownloadError:
            await msg.channel.send(f"Нема таково '{str(url)}'")
            await self.bot.voice_clients[msg.guild.id].disconnect()
            del self.bot.voice_clients[msg.guild.id]
        except Exception as err:
            await msg.channel.send("ГРЕДА")
            if msg.guild.id in self.bot.voice_clients:
                await self.bot.voice_clients[msg.guild.id].disconnect()
                del self.bot.voice_clients[msg.guild.id]
            print(err)
