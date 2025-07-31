import os
import re
import sys
import glob
import random
import yt_dlp
import discord
import asyncio
import datetime
import requests
import functools
import subprocess
from bot_map import *
from io import BytesIO
from collections import deque
from weather_app import get_weather
from PIL import Image, ImageSequence, ImageFilter

from libs.key_loaders import KeyLoader
from libs.dap_holder import DAP
from libs.global_vars import VARS


class BotRunner(VARS):
    def __init__(self):
        super().__init__()
        self.key = KeyLoader.bot_key()
        self.yt_dl_opts = DAP.dlp_options()
        self.ffmpeg_options = DAP.ffmpeg_options()
        self.voice_clients = {}
        self.song_queues = {}
        self.song_queue_name = deque()
        self.ytdl = yt_dlp.YoutubeDL(self.yt_dl_opts)
        self.voice_status = 'not connected'
        self.url = ''
        self.bot_chat = None
        self.client = discord.Client(command_prefix='$', intents=discord.Intents.all())
        self.files_to_clean = []
