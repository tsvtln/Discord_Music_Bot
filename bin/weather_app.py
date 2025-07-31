import requests
from decouple import config


class WeatherApp:
    def __init__(self, city_name):
        self.API_KEY = config('WEATHER_API_KEY')
        self.BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
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
