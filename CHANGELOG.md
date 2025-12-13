# CHANGELOG

## [2.0.3] - 2025-12-13
### Added
- **Random Daily Fact Feature**: The bot now posts a random real-world fact every day at a scheduled time to one or more channels.
    - Facts are fetched from the Useless Facts API, with local fallback facts if the API is unavailable.
    - All facts for the day are tracked in `cache/fact_data.txt` to avoid repeats.
    - The feature is implemented using APScheduler and is fully automated—no user command required.
    - To change the post time or channels, edit the scheduler setup in `bin/events.py`.

## [2.0.2] - 2025-08-21
### Fixes
- Removed duplicated code for handling 5 days weather forecast in `$weather5` command

## [2.0.1] - 2025-08-18
### Feature Enhancements
- GIF messages now timeout for 5 minutes to avoid spam
- Added `$weather5 <city>` command for 5-day weather forecast
- Added the new command to the `$commands` list

## [2.0.0] - 2025-08-07
### MAJOR OVERHAUL - Complete Architecture Restructure
This version represents a complete rewrite and modularization of the Discord Music Bot, moving from a monolithic structure to a clean, modular architecture.

### Added
- **Modular Architecture**: Complete restructure of codebase into separate, specialized modules
- **Event Handlers System**: New `EventHandlers` class in `bin/events.py` for centralized event management
- **Player Module**: Dedicated `Player` class in `bin/player.py` for music playback functionality
- **Command Modules**: Separate handlers for different command types:
  - `on_message/play_commands.py` - Music playback commands ($play, $pause, $resume, $stop, $queue)
  - `on_message/handle_shell_cmds.py` - Shell command execution and security
  - `on_message/lucky_draw.py` - Daily fortune draw functionality ($kysmetche)
  - `on_message/weather_cmd.py` - Weather command handling ($weather)
  - `on_message/keyword_worker.py` - Keyword-based GIF and string responses
- **Global Variables System**: Centralized variable management through `libs/global_vars.py` with `VARS` class inheritance
- **Bot Runner**: New `BotRunner` class in `bin/main.py` for bot lifecycle management
- **Presence Changer**: Dedicated `Presence` class for dynamic bot status updates
- **Weather Integration**: Full weather functionality with OpenWeatherMap API integration
- **Shell Command Security**: Improved security model for allowed/disallowed commands
- **Self-Restart Capability**: Bot can restart its own service when triggered by specific messages

### Changed
- **Complete Code Restructure**: Moved from single-file `LoFi_bot.py` to modular architecture
- **Inheritance Model**: All classes now inherit from `VARS` for shared configuration access
- **Event Registration**: Dynamic event registration system for better organization
- **Error Handling**: Improved error handling and logging across all modules
- **Command Processing**: Streamlined command processing with dedicated handlers
- **Voice State Management**: Enhanced voice state updates for better music continuity
- **GIF Processing**: Consolidated GIF resizing and caching into `KeywordWorker`
- **Configuration Management**: Centralized all bot configuration and variables

### Technical Improvements
- **Separation of Concerns**: Each functionality now has its own dedicated module
- **Code Reusability**: Shared functionality through inheritance and composition
- **Maintainability**: Much easier to maintain, debug, and extend individual features
- **Performance**: Better resource management and reduced memory footprint
- **Scalability**: Modular structure allows for easy feature additions
- **Testing**: Individual modules can be tested independently

### Removed
- **LoFi_bot.py**: Deprecated monolithic bot file (kept in the historical branch)
- **Hardcoded Variables**: Moved all hardcoded values to centralized configuration
- **Duplicate Code**: Eliminated code duplication across functionality

### Migration Notes
- This is a breaking change from previous versions
- All functionality remains the same from user perspective
- Developers should use the new modular structure for any modifications
- The old `LoFi_bot.py` removed and the new `run_bot.py` should be used to start the bot

## [1.1.7]
### Added
- $kysmetche command: Users can now draw a daily fortune ("късметче").
- draw_data.txt: Tracks which users have already drawn their fortune for the day to prevent multiple draws.
- Command prefix list moved to bot_map.py for easier management and cleaner code in LoFi_bot.py.

### Changed
- Updated $commands output to include $kysmetche.
- Refactored command prefix logic to use a shared tuple from bot_map.py.

### Fixed
- Prevented users from drawing more than once per day with $kysmetche.

## [1.1.6]
### Added
- $weather <city> command: The bot can now fetch and display the current weather for a specified city using the OpenWeatherMap API.
- weather_app.py: Added main weather logic, including API integration and error handling.

### Changed
- Weather command output now includes user-friendly error messages for API issues (e.g., invalid key, quota exceeded, city not found).
- Weather command and API key usage now rely on python-decouple for secure configuration.
- Updated command list in $commands to include the new $weather command.

### Fixed
- Typo in GIF dithering constant (FLOYDSTEINBERГ → FLOYDSTEINBERG) for correct GIF processing.
- Improved error handling and debug output for weather API failures.

## [1.1.5]
### Added
- GIF resizing and caching: All GIFs triggered by keywords are now resized to a smaller size (120x120) before being sent to Discord, reducing chat spam and improving usability.
- GIF cache: Resized GIFs are stored in a `gif_cache` folder and reused for future requests, improving performance and reducing bandwidth.
- Improved GIF color handling: Resizing uses Pillow's adaptive palette and dithering for best color preservation within GIF limitations.
- New keyword group: Added `d1` and `d1_keywords` for new GIF triggers.

### Changed
- Updated keyword mapping logic to include the new `d1` group and keywords.
- Updated GIF resizing logic to use Pillow's modern enums for resampling, palette, and dithering (for compatibility and fewer warnings).

### Fixed
- Fixed warnings related to deprecated or missing Pillow constants (LANCZOS, ADAPTIVE, FLOYDSTEINBERG) by using the correct enums.
- Fixed a bug where cached GIFs could be corrupted or not resized properly.
- Improved fallback logic: If GIF resizing fails, the bot now falls back to sending the original GIF URL.

## [1.1.4]
### Added
- Dynamic keyword listing for $key_words command: all keywords are now automatically collected from all keyword lists and mappings, no manual update required.
- Wednesday keyword logic: if a message contains a Wednesday-related keyword, the bot checks the current day and sends a GIF from its_wednesday or not_wednesday accordingly.
- Added new keywords to usl_keywords and wednesday_keywords for improved detection.

### Changed
- Refactored keyword mapping logic for GIFs and string responses to use grouped lists and mappings, improving maintainability and scalability.
- Updated $cmds command to show all allowed OS commands.

### Fixed
- Ensured Wednesday GIF logic only runs if a Wednesday keyword is matched, improving efficiency.
- Fixed dynamic keyword listing to avoid duplicates and always reflect current keyword lists.

## [1.1.1]
### Added
- Allowed shell command mapping for $-prefixed commands (e.g. $date) with custom command execution, using a whitelist from bot_map.py.
- Example: $date runs 'date'.
- Support for sudo commands if configured in allowed_commands and permitted in sudoers (can be a high security issue).

### Changed
- Moved allowed_commands and other mappings to bot_map.py for easier management and less clutter in main code.

### Security
- Only whitelisted commands can be executed via Discord. Arbitrary shell commands are not allowed.

## [1.1.0]
### Added
- Instant music streaming from YouTube (no full download required before playback).
- Whole-word keyword detection for GIF and string responses (e.g., 'бира' but not 'разбирам').
- Support for random GIF selection from a list per keyword.
- Support for keyword-to-string responses (e.g., 'бот' replies with a custom message).

### Changed
- Updated README to reflect new features and usage.

### Fixed
- Prevented blocking of the Discord event loop by running yt_dlp operations in a thread.

## [1.0.0]
- Initial version: basic music playback, queue, and text interface.
