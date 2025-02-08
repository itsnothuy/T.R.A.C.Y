import requests
import os

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    url = f"{BASE_URL}?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city} is {weather_desc}, at {temp}°C."
    else:
        return "I'm sorry, I couldn't fetch the weather info right now."

if __name__ == "__main__":
    print(get_weather("New York"))
