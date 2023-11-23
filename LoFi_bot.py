"""
this works and can play music, needs good upload speed of at least 25Mbps

Dependencies:
discord.py
asyncio
yt_dlp
ffmpeg

To do:
- implement buttons
- implement next song

Done:
- implemented search function
- implemented queue's
- implemented text interface to be displayed in discord of what is currently playing
"""

import discord
import asyncio
import yt_dlp
from collections import deque

# store the bot token in a bot_keys file as plain text
with open('bot_keys', 'r') as f:
    bot_token = f.read().strip()
key = bot_token

# vars
voice_clients = {}
song_queues = {}
yt_dl_opts = {"format": 'bestaudio/best'}
song_queue_name = deque()
ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
voice_status = 'not connected'
url = ''
bot_chat = None
client = discord.Client(command_prefix='$', intents=discord.Intents.all())
ffmpeg_options = {'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 15'}


# queue handler
async def play_next_song(guild_id, msg):  # handles playing songs from the queue
    global bot_chat
    if guild_id in song_queues and song_queues[guild_id]:
        next_url = song_queues[guild_id][0]
        if 'MEGALOVANIA' in get_video_name(next_url):
            bot_chat = 'https://tenor.com/view/funny-dance-undertale-sans-gif-26048955'
        elif "I'VE GOT NO FRIENDS" in get_video_name(next_url):
            bot_chat = 'https://tenor.com/view/actorindie-worlds-smallest-violin-aww-violin-gif-13297153'
        elif 'hipodil' in get_video_name(next_url).lower():
            bot_chat = 'https://tenor.com/view/cat-music-listening-gif-18335467'
        else:
            bot_chat = ''

        if bot_chat:
            await msg.channel.send(bot_chat)
        else:
            await msg.channel.send(f"Пущам: {get_video_name(next_url)}")
        song_queues[guild_id].pop(0)
        song_queue_name.popleft()
        next_song = await asyncio.to_thread(ytdl.extract_info, next_url, {'download': True})
        next_audio = discord.FFmpegPCMAudio(next_song['url'], **ffmpeg_options, executable="/usr/bin/ffmpeg")
        voice_clients[guild_id].play(next_audio,
                                     after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(guild_id, msg),
                                                                                      client.loop))
        await client.change_presence(activity=discord.Game(name=get_video_name(next_url)))


@client.event
async def on_voice_state_update(member, before, after):  # checking voice state and updates accordingly
    if after.channel is None and voice_clients.get(member.guild.id) is not None:
        if not voice_clients[member.guild.id].is_playing() and song_queues.get(member.guild.id):
            await play_next_song(member.guild.id, None)


@client.event
async def on_ready():  # verifies that the bot is started and sets a bot status
    print(f"Bot is ready")
    await client.change_presence(activity=discord.Game(name='цигу мигу чакарака'))


# main handler
@client.event
async def on_message(msg):
    global voice_status, url
    if msg.content.startswith('$play'):
        if voice_status != 'connected':
            try:
                voice_channel = msg.author.voice.channel
                voice_client = await voice_channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
                voice_status = 'connected'
            except Exception as err:
                await msg.channel.send('Влез в music канала.')
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

            if get_video_name(url) != 'Video title not available' and \
                    get_video_name(url) != 'Error retrieving video title':
                await msg.channel.send(f"Добавена песен в плейлиста: {get_video_name(url)}")
                song_queues[msg.guild.id].append(url)
                song_queue_name.append(get_video_name(url))
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
            '$queue - Показва плейлиста'
        ]
        tp = '\n'.join(list_of_commands)
        await msg.channel.send(f"Куманди:\n{tp}")


# helper functions
def get_video_name(youtube_url):  # gets the name of a video/song
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


client.run(key)
