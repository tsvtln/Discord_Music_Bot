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
        self.DAILY_URL = 'https://api.openweathermap.org/data/2.5/forecast/daily'
        self.GEOCODE_URL = 'https://api.openweathermap.org/geo/1.0/direct'
        # Open-Meteo API (free, no API key required)
        self.OPEN_METEO_GEOCODE = 'https://geocoding-api.open-meteo.com/v1/search'
        self.OPEN_METEO_FORECAST = 'https://api.open-meteo.com/v1/forecast'
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

    def _geocode_city(self, city_name):
        """Geocode city name to latitude/longitude via OWM Geocoding API."""
        try:
            r = requests.get(self.GEOCODE_URL, params={'q': city_name, 'limit': 1, 'appid': self.API_KEY}, timeout=5)
            data = r.json()
            if r.status_code != 200 or not isinstance(data, list) or not data:
                return None
            res = data[0]
            return {
                'name': res.get('name'),
                'country': res.get('country'),
                'lat': res.get('lat'),
                'lon': res.get('lon'),
            }
        except Exception:
            return None

    def get_weather15(self, city_name):
        """
        Fetches 16-day weather forecast using Open-Meteo API (completely free, no API key required).
        """
        try:
            # geocode the city name to get coordinates
            geocode_params = {
                'name': city_name,
                'count': 1,
                'language': 'bg',
                'format': 'json'
            }
            geo_response = requests.get(self.OPEN_METEO_GEOCODE, params=geocode_params, timeout=5)
            geo_data = geo_response.json()

            if not geo_data.get('results'):
                return f'Не мой да намеря град "{city_name}".'

            location = geo_data['results'][0]
            lat = location['latitude']
            lon = location['longitude']
            city = location['name']
            country = location.get('country', '')

            # get 16-day forecast using coordinates
            forecast_params = {
                'latitude': lat,
                'longitude': lon,
                'daily': 'temperature_2m_max,temperature_2m_min,weathercode,precipitation_probability_max,windspeed_10m_max,relative_humidity_2m_max',
                'timezone': 'auto',
                'forecast_days': 16
            }
            forecast_response = requests.get(self.OPEN_METEO_FORECAST, params=forecast_params, timeout=8)
            forecast_data = forecast_response.json()

            if 'daily' not in forecast_data:
                return 'Не мой да зема прогнозата.'

            # weather code mapping (WMO Weather interpretation codes)
            weather_codes = {
                0: 'Ясно небе', 1: 'Предимно ясно', 2: 'Частично облачно', 3: 'Облачно',
                45: 'Мъгла', 48: 'Замръзваща мъгла',
                51: 'Лек дъжд', 53: 'Умерен дъжд', 55: 'Силен дъжд',
                61: 'Слаб дъжд', 63: 'Умерен дъжд', 65: 'Силен дъжд',
                71: 'Слаб снеговалеж', 73: 'Умерен снеговалеж', 75: 'Силен снеговалеж',
                80: 'Слаби превалявания', 81: 'Умерени превалявания', 82: 'Силни превалявания',
                95: 'Гръмотевична буря', 96: 'Гръмотевица с град', 99: 'Гръмотевица със силен град'
            }

            # format the forecast
            daily = forecast_data['daily']
            result = []

            for i in range(len(daily['time'])):
                date = daily['time'][i]
                tmax = daily['temperature_2m_max'][i]
                tmin = daily['temperature_2m_min'][i]
                wcode = daily['weathercode'][i]
                weather = weather_codes.get(wcode, f'Код {wcode}')
                humidity = daily['relative_humidity_2m_max'][i]
                wind = daily['windspeed_10m_max'][i]
                precip = daily['precipitation_probability_max'][i] if daily['precipitation_probability_max'][i] else 0

                # monkey patch the rain/snow state, because they have a bug and it shows
                # rain even when it's below freezing
                precip_type = "сняг" if tmax < 2 else "дъжд"

                result.append(
                    f"{date}: {weather}, макс {tmax:.1f}°C, мин {tmin:.1f}°C, {humidity}% увлажнение, {wind:.1f} km/h вятър, {precip}% вероятност за {precip_type}"
                )

            return f"16-дневна прогноза за {city}, {country}:\n" + "\n".join(result)
        except Exception as e:
            return f"Не мой да зема прогнозата. ({str(e)})"

