"""
WeatherApp class to fetch weather data from OpenWeatherMap API.
"""

import requests


class WeatherApp:
    def __init__(self, city_name):
        # Load API key from DB config table
        from bin.db_helpers import DBHelpers
        row = DBHelpers.fetch_one("SELECT config_value FROM config WHERE config_key = %s LIMIT 1", ("WEATHER_API_KEY",))
        if not row or not row[0]:
            raise RuntimeError("WEATHER_API_KEY not set in database config table")
        self.API_KEY = row[0]
        self.BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
        self.FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'
        self.city_name = city_name

    def get_weather(self, city_name):
        """
        Fetches weather data for the given city using OpenWeatherMap API.
        Returns a string with weather info or an error message.
        """
        params = {
            'q': city_name,
            'appid': self.API_KEY,
            'units': 'metric',
            'lang': 'en',
        }
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=5)
            data = response.json()
            # Debug: print the full API response for troubleshooting
            # print(f"Weather API response for {city_name}: {data}")
            if response.status_code != 200 or 'main' not in data:
                # we get only 60 checks per day with the free subscription
                return 'Не намирам града или използвани 60/60 проверки за деня.'
                # Also include the error message from the API if available
                # return f"Could not get weather for '{city_name}'. API says: {data.get('message', 'No details')}"
            weather = data['weather'][0]['description'].capitalize()
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            city = data['name']
            country = data['sys']['country']
            return (f"Времето у {city}, {country}: {weather}\n"
                    f"Температура: {temp}°C (ама е кат {feels_like}°C)\n"
                    f"Увлажнение: {humidity}%\n"
                    f"Ветър: {wind} m/s")
        except Exception as e:
            return f"Error fetching weather: {e}"

    def get_weather5(self, city_name):
        """
        Fetches 5-day weather forecast for the given city using OpenWeatherMap API.
        Returns a string with a summary for each day.
        """
        params = {
            'q': city_name,
            'appid': self.API_KEY,
            'units': 'metric',
            'lang': 'en',
        }
        try:
            response = requests.get(self.FORECAST_URL, params=params, timeout=5)
            data = response.json()
            if response.status_code != 200 or 'list' not in data:
                return 'Не намирам града или използвани 60/60 проверки за деня.'
            # Group forecasts by date
            from collections import defaultdict
            import datetime
            days = defaultdict(list)
            for entry in data['list']:
                dt = datetime.datetime.fromtimestamp(entry['dt'])
                date_str = dt.strftime('%Y-%m-%d')
                days[date_str].append(entry)
            # Prepare a summary for each day (show up to 5 days)
            result = []
            city = data['city']['name']
            country = data['city']['country']
            for i, (date, entries) in enumerate(sorted(days.items())):
                if i >= 5:
                    break
                # Pick the forecast closest to 12:00
                target_hour = 12
                closest = min(entries, key=lambda e: abs(datetime.datetime.fromtimestamp(e['dt']).hour - target_hour))
                weather = closest['weather'][0]['description'].capitalize()
                temp = closest['main']['temp']
                feels_like = closest['main']['feels_like']
                humidity = closest['main']['humidity']
                wind = closest['wind']['speed']
                result.append(
                    f"{date}: {weather}, {temp}°C (кат {feels_like}°C), {humidity}% увлажнение, {wind} m/s вятър"
                )
            return f"5-дневна прогноза за {city}, {country}:\n" + "\n".join(result)
        except Exception as e:
            return f"Error fetching 5-day forecast: {e}"
