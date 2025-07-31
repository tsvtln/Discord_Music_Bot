class DAP:

    @staticmethod
    def dlp_options():
        dlp_ops = {"format": 'bestaudio/best',
                   "restrictfilenames": True,
                   "retry_max": "auto",
                   "noplaylist": True,
                   "nocheckcertificate": True,
                   "quiet": True,
                   "no_warnings": True,
                   "verbose": False,
                   'allow_multiple_audio_streams': True
                   }
        return dlp_ops

    @staticmethod
    def ffmpeg_options():
        ffmpeg_ops = {'options': '-vn -reconnect 15 -reconnect_streamed 15 -reconnect_delay_max 15 -bufsize 64k'}
        return ffmpeg_ops
