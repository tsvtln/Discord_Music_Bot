"""
This module contains helper functions for the Discord Music Bot.
It includes functions for retrieving video names from YouTube URLs,
finding video URLs based on search queries, and cleaning up files.
It also includes a class to suppress YouTube messages in the console output.
"""

import functools

from libs.dap_holder import DAP
import yt_dlp
import asyncio
from libs.global_vars import VARS
import os
import glob
import sys
from datetime import datetime
from typing import Dict, Any, Iterable, Tuple, Optional
import mysql.connector

CONF_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf', 'bot.conf')


def _strip_quotes(val: str) -> str:
    val = val.strip()
    if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
        return val[1:-1]
    return val


class DBHelpers:
    @staticmethod
    def load_conf(path: str = CONF_PATH) -> Dict[str, str]:
        conf: Dict[str, str] = {}
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                key, val = line.split('=', 1)
                conf[key.strip()] = _strip_quotes(val)
        return conf

    @staticmethod
    @functools.lru_cache(maxsize=1)
    def db_conf() -> Dict[str, str]:
        return DBHelpers.load_conf()

    @staticmethod
    def get_conn() -> mysql.connector.MySQLConnection:
        conf = DBHelpers.db_conf()
        db_host = conf.get('DB_HOST', 'localhost')
        db_user = conf.get('DB_USER', 'discord_bot')
        db_pass = conf.get('DB_PASSWORD')
        db_name = conf.get('DB_NAME', 'discord_bot')
        if not db_pass:
            raise RuntimeError('DB_PASSWORD in conf/bot.conf is required to use the database')
        return mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name,
            charset='utf8mb4'
        )

    @staticmethod
    def fetch_one(query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Tuple[Any, ...]]:
        conn = DBHelpers.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def fetch_all(query: str, params: Optional[Tuple[Any, ...]] = None) -> Iterable[Tuple[Any, ...]]:
        conn = DBHelpers.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def execute(query: str, params: Optional[Tuple[Any, ...]] = None) -> None:
        conn = DBHelpers.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
            conn.commit()
        finally:
            conn.close()


class Helpers(VARS):
    # -------- existing helpers below (YouTube, files, timing) --------
    @staticmethod
    # helper functions to get video name from YouTube URL
    def get_video_name_sync(youtube_url):  # blocking version for thread
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                result = ydl.extract_info(youtube_url, download=False)
                if 'title' in result:
                    return result['title']
                else:
                    return "Video title not available"
        except yt_dlp.DownloadError as e:
            print(f"Error: {e}")
            return "Error retrieving video title"

    @staticmethod
    async def get_video_name(youtube_url):  # async wrapper for non-blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, functools.partial(Helpers.get_video_name_sync, youtube_url))

    @staticmethod
    async def find_video_url(search_query):  # async version for non-blocking
        ydl_opts = DAP.dlp_options()

        def _extract():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video = ydl.extract_info(f"ytsearch:{search_query}", ie_key='YoutubeSearch')['entries'][0]
                return video['webpage_url']

        return await asyncio.to_thread(_extract)

    @staticmethod
    async def find_files_to_clean():
        """ collects a list of files to be cleaned"""
        VARS.files_to_clean.clear()
        pattern = os.path.join('.', '*.webm')
        VARS.files_to_clean = glob.glob(pattern)

    @staticmethod
    async def clean_files():
        for file in VARS.files_to_clean:
            os.remove(file)
            print(f"Cleared {file} from local repo")

    @staticmethod
    def time_now_to_seconds():
        time_now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        time_split = time_now.split('-')
        hours, minute, second = time_split[3:]
        total_time = int(hours) * 3600 + int(minute) * 60 + int(second)
        day = int(time_split[2])
        return total_time, day

    @staticmethod
    def anti_spam_check(time_last, day):
        """ checks if the time difference is less than 5 minutes"""
        current_time_to_seconds, day_now = Helpers.time_now_to_seconds()
        if time_last + VARS.timeout <= current_time_to_seconds or day != day_now:
            return True
        return False

    def last_message(self):
        """Sets last message time and day"""
        self.last_message_delta, self.last_message_date = Helpers.time_now_to_seconds()

class SuppressYouTubeMessages:
    """ redirects [youtube] blablabla messages to dev/null"""

    def write(self, message):
        if '[youtube]' not in message or 'File' not in message:
            sys.__stdout__.write(message)

    def flush(self):
        pass

