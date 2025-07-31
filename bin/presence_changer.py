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
# from bot_map import *
import datetime
import requests
from io import BytesIO
from PIL import Image, ImageSequence, ImageFilter
from weather_app import get_weather
from .main import BotRunner
from .helpers import Helpers


class Presence(BotRunner):
    def __init__(self, client):
        super().__init__()
        self.client = client

    async def change_presence_periodically(self):
        while True:
            await self.client.change_presence(activity=discord.Game(name=random.choice(self.presence_states)))
            await asyncio.sleep(1800)  # 30 minutes
