## Discord Bot v2.1.0

> This Python Discord music bot features a modular architecture designed for scalability and maintainability.
> It utilizes discord.py for Discord interactions, asyncio for asynchronous programming, yt_dlp for YouTube, and MySQL for configuration/state.

## Architecture

**Version 2.1.0** introduces database-backed configuration and caching, plus daily maintenance:
- **DB-backed Config & Data**: Keys, commands, keywords, responses, presence states, fortunes, GIFs are loaded from MySQL tables
- **DB GIF Cache**: Resized GIFs are cached in the `gif_cache` DB table instead of the filesystem
- **Daily Maintenance**: APScheduler wipes `draw_data` and `reroll_data` daily at 00:00
- **Event-Driven**: Centralized event handling through the `EventHandlers` class
- **Inheritance System**: Shared configuration through the `VARS` class inheritance model
- **Command Separation**: Individual handlers for different command types

### Project Structure
```
Discord_Music_Bot/
├── run_bot.py                      # Main entry point (uses DB-backed token)
├── CHANGELOG.md                    # Version history
├── README.md                       # Documentation
├── conf/
│   ├── create_discord_bot_db.sql   # DB and user creation (uses session vars)
│   ├── run_with_conf.sh            # Runner to inject secrets from conf/bot.conf
│   ├── run_all.sql                 # Orchestrates modular SQL
│   └── sql/                        # Modular schema + seed data
│       ├── 00_setup.sql
│       ├── 10_config.sql
│       ├── 20_command_prefixes.sql
│       ├── 30_funny_responses.sql
│       ├── 40_gifs.sql
│       ├── 50_presence_states.sql
│       ├── 60_responses.sql
│       ├── 70_fallback_facts.sql
│       ├── 80_keywords.sql
│       ├── 90_allowed_commands.sql
│       ├── 95_list_of_commands.sql
│       ├── 97_lucky_list.sql
│       └── 98_misc.sql             # gif_cache, draw_data, fact_data, reroll_data
├── bin/
│   ├── main.py                     # Bot runner and lifecycle
│   ├── events.py                   # Central event handler coordinator
│   ├── player.py                   # Music playback
│   ├── presence_changer.py         # Dynamic bot status updates
│   ├── weather_app.py              # Weather API integration (DB key)
│   ├── maintenance_scheduler.py    # APScheduler: daily wipes of draw/reroll tables
│   ├── db_helpers.py               # Standalone DB helpers (no libs.* dependency)
│   └── on_message/
│       ├── play_commands.py        # Music commands ($play, $pause, etc.)
│       ├── handle_shell_cmds.py    # Shell command execution (prefix fix; bot-message guard)
│       ├── lucky_draw.py           # Daily fortune ($kysmetche) backed by DB draw/reroll tables
│       ├── weather_cmd.py          # Weather command handler
│       └── keyword_worker.py       # Keyword-based responses; DB GIF cache
├── libs/
│   ├── global_vars.py              # Centralized variable management (DB-backed lists)
│   ├── key_loaders.py              # Loads BOT_KEY & WEATHER_API_KEY from DB
│   ├── daily_fact.py               # Fallback facts from DB; facts stored in DB
│   └── vars/
│       ├── command_prefixes.py     # Command prefixes
│       ├── gifs.py                 # GIF lists loaded from DB
│       ├── presence_states.py      # Presence states from DB
│       ├── os_commands.py          # SSH user/server from conf/bot.conf
│       ├── lucky_list.py           # Fortunes from DB
│       ├── responses.py            # String responses from DB
│       └── funny_responses.py      # Funny not-allowed responses from DB
└── cache/
    └── (no filesystem GIF cache; caching now in DB)
```

## Dependencies

- discord.py
- yt_dlp
- Pillow
- requests
- APScheduler
- mysql-connector-python

Install them using pip:

```bash
pip install -r requirements.txt
```

## Features

### Music Functionality
- Play Music: Stream music in Discord voice channels using YouTube URLs or search queries
- Queue Management: Add multiple songs to queue with automatic sequential playback
- Playback Controls: Pause, resume, and stop commands
- Queue Display: View current song queue with $queue command
- Voice State Management: Automatic queue continuation

### Interactive Features
- Keyword Responses: GIF/text responses from DB-managed keywords
- Dynamic GIF Processing: GIFs resized (120x120) and cached in DB for optimal performance
- Wednesday Logic: Day-aware responses for Wednesday-related keywords
- Weather Integration: Real-time data via $weather <city> (API key from DB)
- Daily Fortune Draw: $kysmetche with per-user tracking in DB (draw_data, reroll_data)
- Shell Command Execution: Secure whitelisted commands (allowed_commands_list from DB)
- Random Daily Fact: Automatic posting of a fact every day (fallback facts from DB)

## Setup and Usage

1. Configure secrets in `conf/bot.conf` (DB credentials, BOT_KEY, WEATHER_API_KEY, SSHUSR, S2)
2. Initialize DB and seed data:
   - `conf/run_with_conf.sh` injects values and runs `conf/run_all.sql`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the bot:
```bash
python run_bot.py
```
5. Invite the bot to your Discord server with appropriate permissions

## Setup

Follow these steps to get the bot running with a MySQL-backed configuration.

1) Install MySQL server (and optionally phpMyAdmin to browse the DB):

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y mysql-server
# Optional: phpMyAdmin
sudo apt install -y phpmyadmin
```

2) Install Python dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

3) Configure `conf/bot.conf` from the example:

```bash
cp conf/bot.conf.example conf/bot.conf
# Edit conf/bot.conf and set DB credentials and keys
# Example keys:
# DB_HOST=localhost
# DB_USER=discord_bot
# DB_PASSWORD=yourStrongDBPassword
# DB_NAME=discord_bot
# BOT_KEY=yourDiscordBotToken
# WEATHER_API_KEY=yourOpenWeatherApiKey
# SSHUSR=yourSSHUser
# S2=yourServerHostOrIP
# timeout=3000
```

4) Populate the database schema and seed data (injecting secrets from `conf/bot.conf`):

```bash
chmod +x conf/run_with_conf.sh
conf/run_with_conf.sh
```

If prompted, enter your MySQL root password. The script will set session variables and source `conf/run_all.sql`, creating the schema and populating tables.

## Configuration

- **DB-backed Variables**: The bot loads configuration and content from MySQL tables:
  - config (BOT_KEY, WEATHER_API_KEY, timeout, SSHUSR, S2)
  - gifs, keyword_groups, keywords, responses, funny_responses, presence_states, lucky_list
  - list_of_commands, allowed_commands_list
- **Secrets Injection**: `run_with_conf.sh` reads from `conf/bot.conf` and sets MySQL session variables

## Maintenance

- **Daily Wipe**: `bin/maintenance_scheduler.py` runs a job at 00:00 to clear `draw_data` and `reroll_data`
- **GIF Cache**: Stored in `gif_cache` table (filename, mime_type, size_bytes, gif_data)

## Notes
- Audio streams directly from YouTube
- All GIF responses are resized and cached in DB
- All modules inherit from `VARS` for shared configuration access
- Security features prevent unauthorized shell command execution

## Random Daily Fact Feature

- Posts a random fact daily at a scheduled time (default in `bin/events.py`)
- Facts fetched from Useless Facts API; fallback facts loaded from DB
- Collected facts stored in `fact_data` table to avoid repeats

### How it works
- At the scheduled time, the bot posts a fact to the configured channels
- If a fact for today already exists, a new unique fact is fetched (up to 50 tries)
- Configure post time and channels in `bin/events.py`

### Example
```
🧠 Daily Fact: Bananas are berries, but strawberries are not.
```

### Configuration
- Channel IDs and post time are set in `bin/events.py` in `start_fact_scheduler`
- Facts are stored in the `fact_data` table
