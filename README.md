## Discord Bot v2.0.0

> This Python Discord music bot features a modular architecture designed for scalability and maintainability.
> It utilizes the discord.py library for Discord interactions, asyncio for asynchronous programming, and yt_dlp for handling YouTube video downloads.
> The bot requires a reliable internet connection with a minimum upload speed of 25Mbps.

## Architecture

**Version 2.0.0** introduces a complete modular restructure:
- **Modular Design**: Separated functionality into specialized modules for better maintainability
- **Event-Driven**: Centralized event handling through the `EventHandlers` class
- **Inheritance System**: Shared configuration through the `VARS` class inheritance model
- **Command Separation**: Individual handlers for different command types

### Project Structure
```
Discord_Music_Bot/
├── run_bot.py                      # Main entry point
├── bin/                            # Core bot modules
│   ├── main.py                     # Bot runner and lifecycle management
│   ├── events.py                   # Central event handler coordinator
│   ├── player.py                   # Music playback functionality
│   ├── presence_changer.py         # Dynamic bot status updates
│   ├── weather_app.py              # Weather API integration
│   └── on_message/                 # Message command handlers
│       ├── play_commands.py        # Music commands ($play, $pause, etc.)
│       ├── handle_shell_cmds.py    # Shell command execution
│       ├── lucky_draw.py           # Daily fortune functionality
│       ├── weather_cmd.py          # Weather command handler
│       └── keyword_worker.py       # Keyword-based responses
├── libs/                           # Shared libraries and configuration
│   ├── global_vars.py              # Centralized variable management
│   ├── key_loaders.py              # API key and token management
│   └── vars/                       # Configuration variables
└── cache/                          # Runtime cache and data
    ├── gif_cache/                  # Resized GIF cache
    └── draw_data.txt               # Daily fortune tracking
```

## Dependencies

    In `requirements.txt`, you will find the necessary dependencies for this project. You can install them using pip.

## Features

### Music Functionality
    • Play Music: Stream music in Discord voice channels using YouTube URLs or search queries, with instant playback
    • Queue Management: Add multiple songs to queue with automatic sequential playback
    • Playback Controls: Pause, resume, and stop commands for full playback control
    • Queue Display: View current song queue with $queue command
    • Voice State Management: Automatic queue continuation when users leave voice channels

### Interactive Features
    • Keyword Responses: Automatic GIF and text responses to specific keywords with intelligent whole-word matching
    • Dynamic GIF Processing: All GIFs are resized (120x120) and cached for optimal Discord performance
    • Wednesday Logic: Special day-aware responses for Wednesday-related keywords
    • Weather Integration: Real-time weather data via $weather <city> command (OpenWeatherMap API)
    • Daily Fortune Draw: $kysmetche command for daily fortune draws with per-user tracking
    • Shell Command Execution: Secure whitelisted shell command execution via Discord

## To Do

    - Buy a new car
    - Learn guitar
    - Drink more water
    - Enjoy life

### Music Commands
- `$play <song/URL>` - Play music from YouTube
- `$pause` - Pause current playback
- `$resume` - Resume paused playback  
- `$stop` - Stop playback and clear queue
- `$queue` - Display current song queue

### Utility Commands
- `$weather <city>` - Get current weather for specified city
- `$kysmetche` - Draw daily fortune (once per day per user)
- `$key_words` - List all available keyword triggers
- `$commands` - Show all available commands
- `$cmds` - List available shell commands

## Setup and Usage

    1. Install dependencies: `pip install -r requirements.txt`
    2. Configure your Discord bot token in the appropriate configuration file
    3. Set up OpenWeatherMap API key for weather functionality
    4. Run the bot: `python run_bot.py`
    5. Invite the bot to your Discord server with appropriate permissions

## Configuration

The bot uses a modular configuration system:
- **Global Variables**: Managed through `libs/global_vars.py`
- **API Keys**: Handled via `libs/key_loaders.py`
- **Command Permissions**: Configured in the security modules
- **Keyword Responses**: Customizable through the vars system

## Migration from v1.x

Version 2.0.0 represents a complete architectural overhaul:
- **Breaking Change**: The monolithic `LoFi_bot.py` is deprecated
- **User Experience**: All commands and functionality remain identical
- **Development**: New modular structure for easier maintenance and feature additions
- **Legacy**: Old bot file kept as reference template

## Notes
- Audio streams directly from YouTube for instant playback without full downloads
- GIF responses are automatically resized and cached for optimal performance  
- All modules inherit from the `VARS` class for shared configuration access
- The modular architecture allows for independent testing and development of features
- Security features prevent unauthorized shell command execution

**Feel free to explore and modify the code based on your preferences and requirements. The modular structure makes it easy to extend functionality or customize behavior. If you encounter any issues or have suggestions, please feel free to contribute or open an issue.**
