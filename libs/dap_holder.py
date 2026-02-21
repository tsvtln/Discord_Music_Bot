"""
Holder for DAP (Discord Audio Player) options.
This class provides static methods to retrieve options for youtube-dl and ffmpeg.
"""
import os

class DAP:

    @staticmethod
    def dlp_options():
        # Ensure cache directory exists
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache')
        os.makedirs(cache_dir, exist_ok=True)

        dlp_ops = {"format": 'bestaudio/best',
                   "restrictfilenames": True,
                   "retry_max": "auto",
                   "noplaylist": True,
                   "nocheckcertificate": True,
                   "quiet": True,
                   "no_warnings": True,
                   "verbose": False,
                   'allow_multiple_audio_streams': True,
                   'outtmpl': os.path.join(cache_dir, '%(title)s-[%(id)s].%(ext)s')
                   }
        return dlp_ops

    @staticmethod
    def ffmpeg_options():
        ffmpeg_ops = {'options': '-vn -reconnect 15 -reconnect_streamed 15 -reconnect_delay_max 15 -bufsize 64k'}
        return ffmpeg_ops
