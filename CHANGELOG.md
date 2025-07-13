# CHANGELOG

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
