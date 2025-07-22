import yt_dlp
from player import Player

class Helpers(Player):
    def __init__(self):
        super().__init__()

    @staticmethod
    # helper functions
    def get_video_name_sync(youtube_url):  # blocking version for thread
        try:
            with yt_dlp.YoutubeDL({}) as ydl:
                result = ydl.extract_info(youtube_url, self.download)
                if 'title' in result:
                    return result['title']
                else:
                    return "Video title not available"
        except yt_dlp.DownloadError as e:
            print(f"Error: {e}")
            return "Error retrieving video title"
