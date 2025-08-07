"""
Weather command handler for the Discord Music Bot
"""
import asyncio
from bin.weather_app import WeatherApp


class WeatherCommandHandler:
    def __init__(self, client):
        self.client = client

    async def handle_weather_command(self, msg):
        """Handle weather command requests"""
        if msg.content.startswith('$weather'):
            parts = msg.content.split(maxsplit=1)
            if len(parts) < 2 or not parts[1].strip():
                return
            city = parts[1].strip()
            weather_app = WeatherApp(city)
            loop = asyncio.get_event_loop()
            weather_info = await loop.run_in_executor(None, weather_app.get_weather, city)
            await msg.channel.send(weather_info)
            return
