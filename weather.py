import requests
import os

WEATHER_API_KEY = os.getenv("caf3beb835074c1bad2104150251002")
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



import requests
import webbrowser

BASE_URL = "https://api.weather.gov"

HEADERS = {
    "User-Agent": "weather-app",
    "Accept": "application/geo+json"
}

def get_grid_info(lat, lon):
    """Get the forecast office and grid information based on latitude and longitude."""
    url = f"{BASE_URL}/points/{lat},{lon}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        grid_info = {
            "forecast_url": data["properties"]["forecast"],
            "hourly_forecast_url": data["properties"]["forecastHourly"],
            "grid_id": data["properties"]["gridId"],
            "grid_x": data["properties"]["gridX"],
            "grid_y": data["properties"]["gridY"],
            "alerts_url": data["properties"]["relativeLocation"]["properties"]["county"],
        }
        return grid_info
    else:
        return None

def get_forecast(url):
    """Fetch the weather forecast from the given NWS forecast URL."""
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        forecast_data = response.json()
        return forecast_data["properties"]["periods"]
    else:
        return None

def get_current_weather(lat, lon):
    """Fetch the current weather forecast."""
    grid_info = get_grid_info(lat, lon)
    if grid_info:
        forecast = get_forecast(grid_info["forecast_url"])
        if forecast:
            current = forecast[0]
            return f"Current weather: {current['detailedForecast']}"
    return "Could not fetch the current weather."

def get_hourly_forecast(lat, lon, hours=6):
    """Fetch the hourly forecast (default: next 6 hours)."""
    grid_info = get_grid_info(lat, lon)
    if grid_info:
        forecast = get_forecast(grid_info["hourly_forecast_url"])
        if forecast:
            hourly_forecast = [f"{period['startTime']}: {period['temperature']}°F, {period['shortForecast']}" for period in forecast[:hours]]
            return "\n".join(hourly_forecast)
    return "Could not fetch the hourly forecast."

def get_weekly_forecast(lat, lon):
    """Fetch the 7-day forecast."""
    grid_info = get_grid_info(lat, lon)
    if grid_info:
        forecast = get_forecast(grid_info["forecast_url"])
        if forecast:
            weekly_forecast = [f"{period['name']}: {period['detailedForecast']}" for period in forecast]
            return "\n".join(weekly_forecast)
    return "Could not fetch the weekly forecast."

def get_weather_alerts(lat, lon):
    """Fetch weather alerts for the given location."""
    grid_info = get_grid_info(lat, lon)
    if grid_info:
        alerts_url = f"{BASE_URL}/alerts/active?area={grid_info['grid_id']}"
        response = requests.get(alerts_url, headers=HEADERS)
        
        if response.status_code == 200:
            alerts_data = response.json()
            if alerts_data["features"]:
                alerts = [f"⚠️ {alert['properties']['headline']}: {alert['properties']['description']}" for alert in alerts_data["features"]]
                return "\n".join(alerts)
            else:
                return "No active weather alerts."
    return "Could not fetch weather alerts."

def get_wind_conditions(lat, lon):
    """Fetch wind speed and direction."""
    grid_info = get_grid_info(lat, lon)
    if grid_info:
        forecast = get_forecast(grid_info["forecast_url"])
        if forecast:
            current = forecast[0]
            return f"Wind: {current['windSpeed']} from {current['windDirection']}"
    return "Could not fetch wind conditions."

def get_uv_index(lat, lon):
    """Fetch the UV index (currently using a static lookup method)."""
    url = f"https://api.weather.gov/gridpoints/{lat},{lon}/stations"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        stations = data["features"]
        if stations:
            return f"UV Index data may be available at: {stations[0]['id']}"
    return "Could not fetch UV Index data."

def show_radar(lat, lon):
    """Open the NWS radar map for the given location."""
    grid_info = get_grid_info(lat, lon)
    if grid_info:
        radar_url = f"https://radar.weather.gov/?station={grid_info['radar_station']}"
        webbrowser.open(radar_url)
        return f"Radar opened: {radar_url}"
    return "Could not fetch radar images."

def get_weather(lat, lon):
    """Fetches current weather conditions from NWS API based on coordinates."""
    url = f"{BASE_URL}/points/{lat},{lon}"
    headers = {"User-Agent": "weather-voice-assistant"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        forecast_url = data["properties"]["forecast"]
        
        forecast_response = requests.get(forecast_url, headers=headers)
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            current = forecast_data["properties"]["periods"][0]
            return f"{current['name']}: {current['detailedForecast']}"
    return "Could not fetch the weather right now."

if __name__ == "__main__":
    # Example location: New York City (40.7128, -74.0060)
    lat, lon = 40.7128, -74.0060

    print("🔹 Current Weather 🔹")
    print(get_current_weather(lat, lon))
    
    print("\n🔹 Hourly Forecast 🔹")
    print(get_hourly_forecast(lat, lon, hours=6))
    
    print("\n🔹 Wind Conditions 🔹")
    print(get_wind_conditions(lat, lon))
    
    
    print("\n🔹 7-Day Forecast 🔹")
    print(get_weekly_forecast(lat, lon))
    
    print("\n🔹 Weather Alerts 🔹")
    print(get_weather_alerts(lat, lon))
    
    print("\n🔹 UV Index 🔹")
    print(get_uv_index(lat, lon))
    
    print("\n🔹 Radar Image 🔹")
    print(show_radar(lat, lon))
