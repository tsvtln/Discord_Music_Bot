"""
this works and can play music, needs good upload speed of at least 25Mbps

Dependencies:
discord.py
asyncio
yt_dlp
ffmpeg

Done:
- implemented search function
- implemented queue's
- implemented text interface to be displayed in discord of what is currently playing
- clean up of downloaded locally files
- improved console logging
"""

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

        # --- Old code (download then play) ---
        # next_song = await asyncio.to_thread(ytdl.extract_info, next_url, {'download': False})
        # next_audio = discord.FFmpegPCMAudio(next_song['url'], **ffmpeg_options, executable="/usr/bin/ffmpeg")
        # await asyncio.sleep(15)

        # --- New code: stream audio directly from YouTube, lower buffer for faster start ---
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

    usl = [
        'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXR0c3duc3R2cnNnMHJzOTd3ZTE1NGxodXkyeDB6M3NiN2plOW0zZiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/dQ5XTlqXTysQdGVdWB/giphy.gif',
        'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cnZlZnl3MmhxZjA0eGFkbmh0aDQzYnN4dTdjZm5wbXJhYTl1MHRuaSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/6JSihSBLPqS1VhO9i2/giphy.gif',
        'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMHZ0cnlzb3Jxb3p1eXlyNDkxZGgwcmwzMWgybnN0OWEwYm92MXpqNyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/iScdi2qu0xfGr8chJq/giphy.gif',
        'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb3pmbDBiY3Vlc3h0OTRzeDhieDdqdzk5ZTM1bHhubjZmenM0aWl2NSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/R9cQo06nQBpRe/giphy.gif',
        'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2IxYWM4bGd1dXhqaDVlb3Q4cWp1ZW54Z3lldXR4bXQwYmJhYjVyZiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Gtnf8Fok8An9m/giphy.gif',
    ]

    beer = [
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExanZhNnFtc2JqcnZkN2p1dXJqdmE4NGRsbTl3cTNuZzFvejV5Y2J5cCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/wKSnAdyvKHKHS/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3RqczhjcjBidDk5cjBrODI3OWk1M25naTZwdG14aDk2cWpjMTNobCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/lTGLOH7ml3poQ6JoFg/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3RqczhjcjBidDk5cjBrODI3OWk1M25naTZwdG14aDk2cWpjMTNobCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/QTgzmGzanMnhiwsBql/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3RqczhjcjBidDk5cjBrODI3OWk1M25naTZwdG14aDk2cWpjMTNobCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l0HlTocc7w1xFoz6g/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ODM4ZmRkZzRwajVyZHZpeWRrdDdpY2JhYmliZDl0eXVwczA1aWQxdyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/1esoXMqqOjYGm5Bdqt/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bzhlNzJwcWN2Ym9tdW1oYnpsamkwaWU0cjljMmJoMTZlbGV4ZWprdyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/9GJ2w4GMngHCh2W4uk/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3MzNiYWVud3FxNXRvdThheHBnNHU0c2IwMTQ3cWlhOGl5YnAyZzdweiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/zTB68FHqA6VRS/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ODFxcXV1MGdoM3F4Z2ttZDY5YmJhZHZpemc3eGR3ZnR3ZDNsbnVwMiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3oEjHNSN9EhhBi2QJq/giphy.gif',
            'https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmdxY3JybjhveWNqYWxjd2U0dTd4NzI4dTN0c3U0eGJ4NjMybmQ0NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26tP21xUQnOCIIoFi/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OXNkcnZva3JxMG5tcnJhZzFsZnhlNjRzNThzMnF6cm9uNW5yeWFiMiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/2AM7sBtPHGTL5r5WFV/giphy.gif',
        ]

    kur = [
            'https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMzkwamt0Z3drOXVncnIwYnZucDRzbDRxdHpwaXBqc3R5ODZuMGp6MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Qc8GJi3L3Jqko/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExamJrZjNpZ3BmYmJybDUyMmpqaHJtcGJpb2dnMDBsZHQ2cm56d2I0aSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/zCOY3loJHTnfG/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExamJrZjNpZ3BmYmJybDUyMmpqaHJtcGJpb2dnMDBsZHQ2cm56d2I0aSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/okEAjcVdCLl4I/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGRsN2k0ZzMwNHd3cG93c2I4cWVvNnp2ZThreTI1Y3RiZzgzN2NseiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/1fkdaiYSkzKGM2a3Wj/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGRsN2k0ZzMwNHd3cG93c2I4cWVvNnp2ZThreTI1Y3RiZzgzN2NseiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l3vRhvmSOagowtJ96/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGRsN2k0ZzMwNHd3cG93c2I4cWVvNnp2ZThreTI1Y3RiZzgzN2NseiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ybpps0dQwaXf2/giphy.gif',
        ]

    funny = [
        'Не съм! Аз съм истински човек!',
        'Къде е Харалампи?',
    ]

    # --- Keyword GIF and string auto-response ---
    keyword_gifs = {
        'car': ['https://media.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.gif'],
        'cat': [
            'https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif',
            'https://media.giphy.com/media/mlvseq9yvZhba/giphy.gif',
            'https://media.giphy.com/media/13borq7Zo2kulO/giphy.gif',
            'https://media.giphy.com/media/12PA1eI8FBqEBa/giphy.gif',
            'https://media.giphy.com/media/OmK8lulOMQ9XO/giphy.gif',
            'https://media.giphy.com/media/6VoDJzfRjJNbG/giphy.gif',
            'https://media.giphy.com/media/10dU7AN7xsi1I4/giphy.gif',
            'https://media.giphy.com/media/krP2NRkLqnKEg/giphy.gif',
            'https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif',
            'https://media.giphy.com/media/5i7umUqAOYYEw/giphy.gif'
        ],
        'dog': ['https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif'],
        'цици': [
            'https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMDBkampxN3Izbmd1OW5tdmVkcjI4Z25iaDI1amg4N2w4bzk1dmFseSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/28A92fQr8uG6Q/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXZ0dnc4bTJyMDl6emw3YXp4dmplMnM3enJ0eHQxeTE0NjQ5Y242MiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/HjlKKc14d5tBK/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3Y3RhaGRmNjd5bTdnNnpsOW8xc2QyenA4c3Q3Z3liYnB2bmdlcHBxZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l378p60yRSCeVoyAM/giphy.gif',
            'https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2x1ZGhpcGp4dWhiczY2ZzdrdjF1MXpseGFqbTNvNnQweXR6cGUxdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QscGFjzLHXVg4/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3Y205OWwyM3B5NW11Nzd4M29tZ2psc3lxOWh4Y3VlNmI3dW5sY2V0dCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/9R2C1v4Y91pp6/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3YW01MGVtZXlva3lyOXc0ZDFlY2w2ODdxNWk5YmQ3MzVyY2h5MW44NCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Q1Q2BRA7CXDGg/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3dGhodDZsNDNpejVuYWZqM2ZqcXc2ZzdyeWRhOWprYWF3bTNmeDIyaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/tQrweyYjPGPjq/giphy.gif',
        ],
        'бири': beer,
        'бира': beer,
        'наздраве': [
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdG1vdXFraDMzbnFtcXRpajR2bXRhb3FmYWwzbGtmdGNndWNjNzQ3aiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Zw3oBUuOlDJ3W/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3I2bzdudGlvdTFxcThiODE3eWMxbmE0NnlwcW90ZXFiZ2VqaTcxayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/4Tkagznwgrv6A4asQb/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3I2bzdudGlvdTFxcThiODE3eWMxbmE0NnlwcW90ZXFiZ2VqaTcxayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l0ExgfAdB2Z9V35hS/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3d2pwM2J4NndvZXRjOWx1cW1xenNzbmNod3JuYzRja2d1dDVzcGEwNyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/RBx8fOTbEmC8iy27Ki/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3aXplMHN4MzNmeWV2bmoyaHIwand0ZGUwYWsxYXc1NTJoNTVpODAzbiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/TujSrrPYXqeAdPnvuh/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OHIyMGJxdWVvOWRoNGx1YW1zYnBnaWVpczhoY3BoeXA1bTJja2cyYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/GvlQffBPPLygHFd43p/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3d2pwM2J4NndvZXRjOWx1cW1xenNzbmNod3JuYzRja2d1dDVzcGEwNyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/hfKTf4RvJJRHL70Zvo/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3aWdxbXo2bmozbTE0OGl0dGFnOG1qemx5YW8zcTRxZTI2ZzIya202bCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l0MYHCPKJ9H2VmRyg/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ZHhja2VzaHo5OTJqdWx4OW1qb21tcG92ZDY3eWdkamdsM3oyZjRlOSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/dXFd3q0msGpMjgNEls/giphy.gif',
            'https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OXJjYWNqc20xMnEzcng5NnhxeGFtbjJvZWR0enNjbnY3Mm14d3FmbSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/cEYFeDYAEZ974cOS8CY/giphy.gif',
        ],
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
        if re.search(rf'(?<!\\w){re.escape(word)}(?!\\w)', lowered):
            await msg.channel.send(response)
            return
    # Then, check for GIF responses
    for word, gif_list in keyword_gifs.items():
        if re.search(rf'(?<!\\w){re.escape(word)}(?!\\w)', lowered):
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
