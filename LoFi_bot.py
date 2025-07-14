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

# store the bot token in a bot_keys file as plain text
with open('bot_keys', 'r') as f:
    bot_token = f.read().strip()
key = bot_token

# vars
voice_clients = {}
song_queues = {}
yt_dl_opts = {"format": 'bestaudio/best',
              "restrictfilenames": True,
              "retry_max": "auto",
              "noplaylist": True,
              "nocheckcertificate": True,
              "quiet": True,
              "no_warnings": True,
              "verbose": False,
              'allow_multiple_audio_streams': True
              }
ffmpeg_options = {
    'options': '-vn -reconnect 15 -reconnect_streamed 15 -reconnect_delay_max 15'
}
song_queue_name = deque()
ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
voice_status = 'not connected'
url = ''
bot_chat = None
client = discord.Client(command_prefix='$', intents=discord.Intents.all())
files_to_clean = []


# queue handler
async def play_next_song(guild_id, msg):  # handles playing songs from the queue
    global bot_chat
    if guild_id in song_queues and song_queues[guild_id]:
        next_url = song_queues[guild_id][0]
        video_name = await get_video_name(next_url)
        if 'MEGALOVANIA' in video_name:
            bot_chat = 'https://tenor.com/view/funny-dance-undertale-sans-gif-26048955'
        elif "I'VE GOT NO FRIENDS" in video_name:
            bot_chat = 'https://tenor.com/view/actorindie-worlds-smallest-violin-aww-violin-gif-13297153'
        elif 'hipodil' in video_name.lower():
            bot_chat = 'https://tenor.com/view/cat-music-listening-gif-18335467'
        else:
            bot_chat = ''

        if bot_chat:
            await msg.channel.send(bot_chat)
        else:
            await msg.channel.send(f"Пущам: {video_name}")
        # clean up
        song_queues[guild_id].pop(0)
        song_queue_name.popleft()
        await find_files_to_clean()
        if len(files_to_clean) >= 10:
            await clean_files()

        # Stream audio directly from YouTube, lower buffer for faster start
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, functools.partial(ytdl.extract_info, next_url, download=False))
        audio_url = info['url']
        ffmpeg_stream_options = ffmpeg_options.copy()
        ffmpeg_stream_options['options'] += ' -bufsize 64k'
        next_audio = discord.FFmpegPCMAudio(audio_url, **ffmpeg_stream_options, executable="/usr/bin/ffmpeg")
        voice_clients[guild_id].play(next_audio,
                                     after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(guild_id, msg),
                                                                                      client.loop))
        await client.change_presence(activity=discord.Game(name=video_name))


async def change_presence_periodically():
    while True:
        await client.change_presence(activity=discord.Game(name=random.choice(presence_states)))
        await asyncio.sleep(1800)  # 30 minutes


@client.event
async def on_voice_state_update(member, before, after):  # checking voice state and updates accordingly
    if after.channel is None and voice_clients.get(member.guild.id) is not None:
        if not voice_clients[member.guild.id].is_playing() and song_queues.get(member.guild.id):
            await play_next_song(member.guild.id, None)


@client.event
async def on_ready():  # verifies that the bot is started and sets a bot status
    print(f"Bot is ready")
    client.loop.create_task(change_presence_periodically())
    await client.change_presence(activity=discord.Game(name=random.choice(presence_states)))


# main handler
@client.event
async def on_message(msg):
    global voice_status, url
    await handle_shell_command(msg)

    # --- Keyword GIF and string auto-response ---
    keyword_gifs = {
        'car': ['https://media.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.gif'],
        'cat': ['https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif'],
        'dog': ['https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif'],
        'цици': booba,
        'бири': beer,
        'бира': beer,
        'bira': beer,
        'biri': beer,
        'beer': beer,
        'наздраве': cheer,
        'кур': kur,
        'курец': kur,
        'курове': kur,
        'кура': kur,
        'useless': usl,
        'uselessa': usl,
        'юслес': usl,
        'юслеса': usl,
        'ангел': usl,
        'ачо': usl,
    }

    keyword_strings = {
        'бот': funny[0],
        'бота': funny[0],
        'ботче': funny[0],
        'bot': funny[0],
        'haralampi': funny[1],
        'харалампи': funny[1],
    }

    lowered = msg.content.lower()
    # First, check for string responses
    for word, response in keyword_strings.items():
        if re.search(rf'\\b{re.escape(word)}\\b', lowered):
            await msg.channel.send(response)
            return
    # Then, check for GIF responses
    for word, gif_list in keyword_gifs.items():
        if re.search(rf'\\b{re.escape(word)}\\b', lowered):
            await msg.channel.send(random.choice(gif_list))
            return

    if msg.content.startswith('$play'):
        if voice_status != 'connected':
            try:
                voice_channel = msg.author.voice.channel
                voice_client = await voice_channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
                voice_status = 'connected'
            except Exception as err:
                await msg.channel.send('Влез във voice канал, иначе тре серенада пред блока ти праа.')
                voice_status = 'not connected'
                print(err)
                raise NotInVoiceChannel

        try:
            test_for_url = msg.content.split()
            if len(test_for_url) > 1:
                test_for_url = deque(test_for_url[1:])
                url = ' '.join(test_for_url)
            else:
                url = test_for_url[1]

            if url == 'skakauec':
                url = 'https://www.youtube.com/watch?v=pq3C-UE6RE0'
            elif url == 'sans':
                url = 'https://www.youtube.com/watch?v=0FCvzsVlXpQ'
            elif url == 'ignf':
                url = 'https://www.youtube.com/watch?v=yLnd3AYEd2k'
            elif 'http' not in url:
                url = find_video_url(url)

            if msg.guild.id not in song_queues:
                song_queues[msg.guild.id] = []

            video_name = await get_video_name(url)
            if video_name != 'Video title not available' and \
                    video_name != 'Error retrieving video title':
                await msg.channel.send(f"Добавена песен в плейлиста: {video_name}")
                song_queues[msg.guild.id].append(url)
                song_queue_name.append(video_name)
            else:
                await msg.channel.send('Пробуем при намирането на таз песен.')

            if len(song_queues[msg.guild.id]) == 1 and not voice_clients[msg.guild.id].is_playing():
                await play_next_song(msg.guild.id, msg)

        except yt_dlp.DownloadError:
            await msg.channel.send(f"Нема такова '{str(url)}'")
            await voice_clients[msg.guild.id].disconnect()
            voice_status = 'not connected'
        except Exception as err:
            await msg.channel.send("ГРЕДА")  # if this is printed in discord, something is broken
            await voice_clients[msg.guild.id].disconnect()
            voice_status = 'not connected'
            print(err)

    if msg.content.startswith("$pause"):
        try:
            voice_clients[msg.guild.id].pause()
        except Exception as err:
            print(err)

    if msg.content.startswith("$resume"):
        try:
            voice_clients[msg.guild.id].resume()
        except Exception as err:
            print(err)

    if msg.content.startswith("$stop"):
        try:
            voice_clients[msg.guild.id].stop()
            await voice_clients[msg.guild.id].disconnect()
            voice_status = 'not connected'
            del song_queues[msg.guild.id]
            song_queue_name.clear()
        except Exception as err:
            print(err)

    if msg.content.startswith("$key_words"):
        keywords = [
            'car', 'cat', 'dog', 'цици', 'бири', 'бира', 'beer',
            'наздраве', 'кур', 'курец', 'курове', 'кура',
            'useless', 'uselessa', 'юслес', 'юслеса',
            'ангел', 'ачо'
        ]
        await msg.channel.send(f"Ключови думи:\n{', '.join(keywords)}")

    if msg.content.startswith("$queue"):
        if msg.guild.id in song_queues and song_queue_name:
            formatted_queue = [f"{i}. {name}" for i, name in enumerate(song_queue_name, 1)]
            queue_list = '\n'.join(formatted_queue)
            await msg.channel.send(f"Плейлист:\n{queue_list}")
        else:
            await msg.channel.send('Нема плейлист')

    if msg.content.startswith("$commands"):
        list_of_commands = [
            '$play (url или име на песен) - Пуща песен',
            '$pause - Палза',
            '$stop - Спира песента и трие све',
            '$resume - Пуща паузираната песен',
            '$queue - Показва плейлиста',
            '$key_words - Показва ключови думи',
        ]
        tp = '\n'.join(list_of_commands)
        await msg.channel.send(f"Куманди:\n{tp}")


async def handle_shell_command(msg):
    # Handles shell commands sent by users
    if msg.content.startswith('$') and not msg.content.startswith(('$play', '$pause', '$resume', '$stop', '$queue', '$commands')):
        cmd_key = msg.content[1:].strip()
        if cmd_key in allowed_commands:
            command = allowed_commands[cmd_key]
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
                output = result.stdout.strip() or result.stderr.strip() or 'No output.'
                if len(output) > 1900:
                    output = output[:1900] + '\n...output truncated...'
                await msg.channel.send(f'```{output}```')
            except Exception as e:
                await msg.channel.send(f'Error running command: {e}')
        elif cmd_key in not_allowed:
            await msg.channel.send(not_allowed[cmd_key])
        else:
            await msg.channel.send('https://media.giphy.com/media/NpdriuxQAXJ7Hsst1R/giphy.gif')


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


async def get_video_name(youtube_url):  # async wrapper for non-blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, functools.partial(get_video_name_sync, youtube_url))


def find_video_url(search_query):  # gets the pure url to a video, based only a search query
    ydl_opts = yt_dl_opts
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video = ydl.extract_info(f"ytsearch:{search_query}", ie_key='YoutubeSearch')['entries'][0]
        return video['webpage_url']


class NotInVoiceChannel(Exception):
    """A custom exception class to raise an error if user is not in a voice channel."""

    def __init__(self, message="User not in voice channel."):
        self.message = message
        super().__init__(self.message)


async def find_files_to_clean():
    """ collects a list of files to be cleaned"""
    global files_to_clean
    files_to_clean.clear()
    pattern = os.path.join('.', '*.webm')
    files_to_clean = glob.glob(pattern)


async def clean_files():
    global files_to_clean
    for file in files_to_clean:
        os.remove(file)
        print(f"Cleared {file} from local repo")


class SuppressYouTubeMessages:
    """ redirects [youtube] blablabla messages to dev/null"""
    def write(self, message):
        if '[youtube]' not in message or 'File' not in message:
            sys.__stdout__.write(message)

    def flush(self):
        pass


sys.stdout = SuppressYouTubeMessages()
client.run(key)
