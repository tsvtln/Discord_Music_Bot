# CHANGELOG

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
