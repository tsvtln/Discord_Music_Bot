## Discord Bot v2.2.0

> This Python Discord music bot features a modular architecture designed for scalability and maintainability.
> It utilizes discord.py for Discord interactions, asyncio for asynchronous programming, yt_dlp for YouTube, and MySQL for configuration/state.

## Architecture

**Version 2.2.0** introduces Ansible job status monitoring and reporting:
- **Ansible Job Status Scheduler**: Automated monitoring and posting of Ansible job execution results from Semaphore
- **DB-backed Config & Data**: Keys, commands, keywords, responses, presence states, fortunes, GIFs are loaded from MySQL tables
- **DB GIF Cache**: Resized GIFs are cached in the `gif_cache` DB table instead of the filesystem
- **Daily Maintenance**: APScheduler wipes `draw_data` and `reroll_data` daily at 00:00
- **Event-Driven**: Centralized event handling through the `EventHandlers` class
- **Inheritance System**: Shared configuration through the `VARS` class inheritance model
- **Command Separation**: Individual handlers for different command types

### Project Structure
```
Discord_Music_Bot/
├── bin
│   ├── artifical_bot.py
│   ├── db_helpers.py
│   ├── events.py
│   ├── helpers.py
│   ├── __init__.py
│   ├── main.py
│   ├── maintenance_scheduler.py
│   ├── on_message
│   │   ├── handle_shell_cmds.py
│   │   ├── keyword_worker.py
│   │   ├── lucky_draw.py
│   │   ├── play_commands.py
│   │   ├── __pycache__
│   │   │   ├── handle_shell_cmds.cpython-312.pyc
│   │   │   ├── keyword_worker.cpython-312.pyc
│   │   │   ├── lucky_draw.cpython-312.pyc
│   │   │   ├── play_commands.cpython-312.pyc
│   │   │   └── weather_cmd.cpython-312.pyc
│   │   └── weather_cmd.py
│   ├── player.py
│   ├── presence_changer.py
│   ├── __pycache__
│   │   ├── artifical_bot.cpython-312.pyc
│   │   ├── db_helpers.cpython-312.pyc
│   │   ├── events.cpython-312.pyc
│   │   ├── helpers.cpython-312.pyc
│   │   ├── __init__.cpython-312.pyc
│   │   ├── main.cpython-312.pyc
│   │   ├── maintenance_scheduler.cpython-312.pyc
│   │   ├── player.cpython-312.pyc
│   │   ├── presence_changer.cpython-312.pyc
│   │   └── weather_app.cpython-312.pyc
│   └── weather_app.py
├── CHANGELOG.md
├── conf
│   ├── bot.conf
│   ├── bot.conf.example
│   ├── create_discord_bot_db.sql
│   ├── run_all.sql
│   ├── run_with_conf.sh
│   └── sql
│       ├── 00_setup.sql
│       ├── 10_config.sql
│       ├── 20_command_prefixes.sql
│       ├── 30_funny_responses.sql
│       ├── 40_gifs.sql
│       ├── 50_presence_states.sql
│       ├── 60_responses.sql
│       ├── 70_fallback_facts.sql
│       ├── 80_keywords.sql
│       ├── 90_allowed_commands.sql
│       ├── 95_list_of_commands.sql
│       ├── 97_lucky_list.sql
│       └── 98_misc.sql
├── libs
│   ├── daily_fact.py
│   ├── dap_holder.py
│   ├── global_vars.py
│   ├── __init__.py
│   ├── key_loaders.py
│   ├── __pycache__
│   │   ├── daily_fact.cpython-312.pyc
│   │   ├── dap_holder.cpython-312.pyc
│   │   ├── global_vars.cpython-312.pyc
│   │   ├── __init__.cpython-312.pyc
│   │   └── key_loaders.cpython-312.pyc
│   └── vars
│       ├── command_prefixes.py
│       ├── funny_responses.py
│       ├── gifs.py
│       ├── __init__.py
│       ├── lucky_list.py
│       ├── os_commands.py
│       ├── presence_states.py
│       ├── __pycache__
│       │   ├── command_prefixes.cpython-312.pyc
│       │   ├── funny_responses.cpython-312.pyc
│       │   ├── gifs.cpython-312.pyc
│       │   ├── __init__.cpython-312.pyc
│       │   ├── lucky_list.cpython-312.pyc
│       │   ├── os_commands.cpython-312.pyc
│       │   ├── presence_states.cpython-312.pyc
│       │   └── responses.cpython-312.pyc
│       └── responses.py
├── LICENSE
├── README.md
├── requirements.txt
└── run_bot.py
```

## Dependencies

The bot requires the following Python packages (see requirements.txt for the full list):

- discord.py
- yt_dlp
- Pillow
- requests
- APScheduler
- mysql-connector-python
- anthropic
- langchain
- langchain-anthropic
- langchain-core
- langgraph
- langgraph-checkpoint
- langgraph-prebuilt
- langgraph-sdk
- langsmith
- python-decouple
- PyYAML
- selenium
- beautifulsoup4
- pytest
- ffmpeg
- aiohttp
- trio
- sortedcontainers
- typing-inspection
- typing_extensions
- orjson
- soupsieve
- PyNaCl
- PySocks
- uuid_utils
- zstandard
- ...and more utility packages (see requirements.txt)

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
- Haralampi keyword responses: AI-powered or database-powered, toggleable at runtime
- $ChatMode command: Switches Haralampi between AI and DB response modes
- Custom user data: Store and retrieve arbitrary user data from MySQL
- **Ansible Job Status Monitoring**: Automated monitoring and posting of Ansible job execution results from Semaphore server

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

_NOTE:_ You will have to manually populate the table. Also, might need to adjust the prompt to your liking in 
bin/artifical_bot.py. Additionally need to manually populate the list for your discord users in libs/global_vars.py users_for_chat_mode()

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

## Haralampi AI/DB Toggle and $ChatMode Command

### Haralampi Chat Modes
- The bot supports two modes for Haralampi keyword responses:
  - **AI Mode**: Uses Claude 3 Haiku for intelligent, contextual, and personalized responses (with memory)
  - **Database Mode**: Uses fast, simple, predefined responses from the database
- Toggle between modes using the `$ChatMode` command in Discord. The bot will confirm the current mode.
- Default mode is AI (can be changed at runtime, not persistent across restarts).

### $ChatMode Command
- Type `$ChatMode` in Discord to switch between AI and database response modes for Haralampi.
- The bot will reply with the current mode status ("AI Bot (Intelligent)" or "Database (Simple)").
- When in AI mode, Haralampi uses memory and user-specific behavior. In database mode, responses are instant and simple.

### Custom User Data Table
- The bot now supports a `custom_user_data` table for storing arbitrary user-specific data.
- Table schema:
  ```sql
  CREATE TABLE custom_user_data (
      user_key VARCHAR(64) PRIMARY KEY,
      user_value TEXT NOT NULL
  );
  ```
- Data can be loaded using the `_load_custom_user_data()` method in code.

## Ansible Job Status Monitoring

### Overview
- The bot automatically monitors and reports Ansible job execution status from a Semaphore server
- Runs on a scheduled basis (default: daily at 18:31) and posts results to a configured Discord channel
- Fetches job data via Semaphore REST API using Bearer token authentication
- Parses job output to extract meaningful information like template names, execution status, and package upgrade summaries

### How it works
1. At the scheduled time, the bot retrieves the next job ID from the `job_id_tracker` table in MySQL
2. Fetches the job's raw output and status from Semaphore API endpoints:
   - `/api/project/1/tasks/{job_id}/raw_output` - Full job output
   - `/api/project/1/tasks/{job_id}` - Job status summary
3. Parses the output to extract:
   - Template name and execution status
   - Package upgrade summaries
   - Job summary output
4. Posts formatted results to the configured Discord channel
5. Increments the job ID tracker in the database for the next run
6. Continues checking jobs until an invalid/missing job is encountered

### Configuration
- **Channel ID**: Set in `bin/events.py` in the `send_ansible_job_status` method (default: `1474763280970027070`)
- **Schedule**: Configured using CronTrigger in the same method (default: `hour=18, minute=31`)
- **API Key**: Stored in the `config` table with key `semaphore_api_key`
- **Job Tracker**: Uses the `job_id_tracker` table to maintain the current job ID

### Database Requirements
- `job_id_tracker` table with a single `job_id` integer field
- `config` table entry with `config_key='semaphore_api_key'` containing your Semaphore API Bearer token

### Example Output
```
Ansible Playbook: System Updates - success
============================================
Updated packages:
  - package1: 1.0.0 -> 1.0.1
  - package2: 2.3.4 -> 2.3.5
```

### SQL Setup
```sql
-- Create job_id_tracker table
CREATE TABLE IF NOT EXISTS job_id_tracker (
    job_id INT
);

-- Insert initial job ID
INSERT INTO job_id_tracker (job_id) VALUES (1);

-- Add Semaphore API key to config table
INSERT INTO config (config_key, config_value) 
VALUES ('semaphore_api_key', 'YOUR_SEMAPHORE_BEARER_TOKEN');
```

