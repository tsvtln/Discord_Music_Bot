"""
Discord Music Bot Player Module
Handles playing music in a Discord voice channel.
This module is responsible for managing the playback of songs in a Discord voice channel,
Since now it's in OOP it is being able to play songs in multiple channels simultaneously.
Yes I know, that is mind-boggling, I'm so smart, right?
"""

import discord
import asyncio
import functools
from .main import BotRunner
from .helpers import Helpers
from libs.global_vars import VARS


class Player(BotRunner, VARS):
    def __init__(self, guild_id, msg, bot_instance=None):
        super().__init__()
        self.guild_id = guild_id
        self.msg = msg
        self.bot_instance = bot_instance or self
        self.next_url = ''
        self.youtube_url = ''
        self.video_name = ''
        self.download = False
        self.next_audio = ''
        self.bot_chat = ''

    async def get_video_name(self, youtube_url):  # async wrapper for non-blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, functools.partial(Helpers.get_video_name_sync, youtube_url))

    async def play_next_song(self):
        # Access bot instance variables correctly
        if hasattr(self.bot_instance, 'song_queues'):
            song_queues = self.bot_instance.song_queues
            voice_clients = self.bot_instance.voice_clients
            song_queue_name = self.bot_instance.song_queue_name
            client = self.bot_instance.client
        else:
            song_queues = self.song_queues
            voice_clients = self.voice_clients
            song_queue_name = self.song_queue_name
            client = self.client

        if self.guild_id in song_queues and song_queues[self.guild_id]:
            # Get the song data (url, video_name, audio_url) from queue
            next_song_data = song_queues[self.guild_id][0]
            self.next_url = next_song_data[0]  # URL
            self.video_name = next_song_data[1]  # Video name
            audio_url = next_song_data[2]  # Audio URL

            # Check for special songs and send appropriate GIFs
            if 'MEGALOVANIA' in self.video_name:
                self.bot_chat = 'https://tenor.com/view/funny-dance-undertale-sans-gif-26048955'
            elif "I'VE GOT NO FRIENDS" in self.video_name:
                self.bot_chat = 'https://tenor.com/view/actorindie-worlds-smallest-violin-aww-violin-gif-13297153'
            elif 'hipodil' in self.video_name.lower():
                self.bot_chat = 'https://tenor.com/view/cat-music-listening-gif-18335467'
            else:
                self.bot_chat = ''

            # Send GIF or playing message
            if self.bot_chat and self.msg:
                await self.msg.channel.send(self.bot_chat)
            elif self.msg:
                await self.msg.channel.send(f"Пущам: {self.video_name}")

            # Clean up queue
            song_queues[self.guild_id].pop(0)
            if song_queue_name:
                song_queue_name.popleft()

            # Create audio source and play
            self.next_audio = discord.FFmpegPCMAudio(audio_url, **self.ffmpeg_options, executable="/usr/bin/ffmpeg")

            # Play the audio with callback for next song
            # Ignore the false warning on the run_coroutine_threadsafe
            voice_clients[self.guild_id].play(self.next_audio,
                                               after=lambda e: asyncio.run_coroutine_threadsafe(
                                                   self.play_next_song(),
                                                   client.loop))

            # Update bot presence
            await client.change_presence(activity=discord.Game(name=self.video_name))
