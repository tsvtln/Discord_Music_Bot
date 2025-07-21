import discord
import asyncio
import yt_dlp
from collections import deque
import os
import glob
import sys
import functools
import random
import re
import subprocess
from bot_map import *
import datetime
import requests
from io import BytesIO
from PIL import Image, ImageSequence, ImageFilter
from weather_app import get_weather
from main import BotRunner
from helpers import Helpers as help

class Player(BotRunner):
    def __init__(self, guild_id, msg):
        super().__init__()
        self.guild_id = guild_id
        self.msg = msg
        self.next_url = ''
        self.youtube_url = ''
        self.video_name = ''
        self.download = False

    async def get_video_name(self, youtube_url):  # async wrapper for non-blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, functools.partial(help.get_video_name_sync, self.youtube_url))
    
    async def play_next_song(self):
        if self.guild_id in self.song_queues and self.song_queues[self.guild_id]:
            self.next_url = self.song_queues[self.guild_id][0]
            self.video_name = await self.get_video_name(self.next_url)
            if 'MEGALOVANIA' in self.video_name:
                self.bot_chat = 'https://tenor.com/view/funny-dance-undertale-sans-gif-26048955'
            elif "I'VE GOT NO FRIENDS" in self.video_name:
                self.bot_chat = 'https://tenor.com/view/actorindie-worlds-smallest-violin-aww-violin-gif-13297153'
            elif 'hipodil' in self.video_name.lower():
                self.bot_chat = 'https://tenor.com/view/cat-music-listening-gif-18335467'
            else:
                self.bot_chat = ''

            if self.bot_chat:
                await self.msg.channel.send(self.bot_chat)
            else:
                await self.msg.channel.send(f"Пущам: {self.video_name}")
            
            # clean up
            self.song_queues[self.guild_id].pop(0)
            self.song_queue_name.popleft()
            
            """ Defunct part. We don't download files anymore. """
            # await self.find_files_to_clean()
            # if len(self.files_to_clean) >= 10:
            #     await self.clean_files()

            # Stream audio directly from YouTube, lower buffer for faster start
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, functools.partial(self.ytdl.extract_info, self.next_url, self.download))
            audio_url = info['url']

            """ Since we will only stream audio we dont need to copy the options, as only 1 version will be used"""
            # ffmpeg_stream_options = self.ffmpeg_options.copy()
            # ffmpeg_stream_options['options'] += ' -bufsize 64k'
            # next_audio = discord.FFmpegPCMAudio(audio_url, **ffmpeg_stream_options, executable="/usr/bin/ffmpeg")

            self.next_audio = discord.FFmpegPCMAudio(audio_url, **self.ffmpeg_options, executable="/usr/bin/ffmpeg")
            self.voice_clients[self.guild_id].play(self.next_audio,
                                        after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next_song(self.guild_id, self.msg),
                                                                                        self.client.loop))
            await self.client.change_presence(activity=discord.Game(name=self.video_name))
