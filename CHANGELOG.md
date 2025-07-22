# CHANGELOG

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

