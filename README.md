## Music Bot

> This Python script is a Discord music bot designed to play music in voice channels.
> It utilizes the discord.py library for Discord interactions, asyncio for asynchronous programming, and yt_dlp for handling YouTube video downloads.
> The bot requires a reliable internet connection with a minimum upload speed of 25Mbps.

## Dependencies

    In `requirements.txt`, you will find the necessary dependencies for this project. You can install them using pip.

## Features

    • Play Music: The bot can play music in a Discord voice channel using YouTube URLs or search queries, streaming audio instantly without waiting for full download.
    • Queue Management: Users can add songs to the queue, and the bot will play them in order.
    • Text Interface: The bot displays the current playing song in the Discord chat.
    • Pause, Resume, Stop: Users can control playback with commands to pause, resume, or stop the current song.
    • Queue Display: Users can check the current queue of songs.
    • Keyword GIF & String Responses: The bot automatically responds to messages containing specific keywords with random GIFs or custom text responses, using whole-word matching (e.g., 'бира' but not 'разбирам').
    • Dynamic keyword listing: The $key_words command now lists all keywords automatically from all keyword lists and mappings.
    • Wednesday keyword logic: If a message contains a Wednesday-related keyword, the bot checks the current day and sends a GIF from its_wednesday or not_wednesday accordingly.
    • All keyword and GIF/string mappings are grouped for easier maintenance and scalability.

## To Do

    - Buy a new car
    - Learn guitar
    - Drink more water
    - Enjoy life

## Done

    - Implemented search function.
    - Implemented queues for managing multiple songs.
    - Implemented a text interface to display the currently playing song in Discord.
    - Refactored keyword mapping logic for maintainability and scalability.
    - Added dynamic keyword listing and Wednesday logic.

## Usage

    1. Make sure to have the required dependencies installed.
    2. Store your Discord bot token in a file named bot_keys.
    3. Run the script, and the bot will be ready to join voice channels and play music.

## Notes
    The bot currently will download the video in webm format 251, which helps if you have slower connection.
    To disable this change {'download': True} to False

**Feel free to explore and modify the code based on your preferences and requirements. If you encounter any issues or have suggestions, please feel free to contribute or open an issue.**
