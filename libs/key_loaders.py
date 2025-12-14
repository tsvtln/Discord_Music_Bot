"""
KeyLoader class to load bot keys and API keys from MySQL config table.
"""
from typing import Tuple
import functools


class KeyLoader:

    @staticmethod
    @functools.lru_cache(maxsize=128)
    def _get_config_value(key: str) -> str:
        # Local import to avoid circular init
        from bin.db_helpers import DBHelpers
        row = DBHelpers.fetch_one("SELECT config_value FROM config WHERE config_key = %s LIMIT 1", (key,))
        if not row:
            raise KeyError(f"Config key '{key}' not found in database")
        return row[0]

    @staticmethod
    def bot_key() -> str:
        return KeyLoader._get_config_value('BOT_KEY')

    @staticmethod
    def weather_loader() -> Tuple[str, str]:
        api_key = KeyLoader._get_config_value('WEATHER_API_KEY')
        base_url = 'https://api.openweathermap.org/data/2.5/weather'
        return api_key, base_url
