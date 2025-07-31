import os
from decouple import config


class KeyLoader:

    @staticmethod
    # store the bot token in a bot_keys file as plain text
    def bot_key():
        with open('bot_keys', 'r') as f:
            bot_token = f.read().strip()
        bot_key = bot_token
        return bot_key

    @staticmethod
    def weather_loader():
        API_KEY = config('WEATHER_API_KEY')
        BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
        return API_KEY, BASE_URL
