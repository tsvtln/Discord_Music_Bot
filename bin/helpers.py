import yt_dlp

class Helpers:
    @staticmethod
    # helper functions
    def get_video_name_sync(youtube_url):  # blocking version for thread
        try:
            with yt_dlp.YoutubeDL({}) as ydl:
                result = ydl.extract_info(youtube_url, download=False)
                if 'title' in result:
                    return result['title']
                else:
                    return "Video title not available"
        except yt_dlp.DownloadError as e:
            print(f"Error: {e}")
            return "Error retrieving video title"
