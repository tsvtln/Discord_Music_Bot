import functools
from libs.dap_holder import DAP
import yt_dlp
import asyncio
from libs.global_vars import VARS
import os
import glob
import sys


class Helpers:
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


class SuppressYouTubeMessages:
    """ redirects [youtube] blablabla messages to dev/null"""

    def write(self, message):
        if '[youtube]' not in message or 'File' not in message:
            sys.__stdout__.write(message)

    def flush(self):
        pass