import aiohttp

from app.services.cache_service import (
    get_cached_weather,
    save_weather_cache,
)

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


async def get_weather(latitude: float, longitude: float):
    cache_key = f"{round(latitude, 2)}:{round(longitude, 2)}"

    cached = await get_cached_weather(cache_key)

    if cached:
        return cached

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "apparent_temperature",
            "wind_speed_10m",
            "relative_humidity_2m",
            "weather_code",
        ],
        "hourly": [
            "temperature_2m",
            "precipitation_probability",
            "weather_code",
            "wind_speed_10m",
        ],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
            "weather_code",
        ],
        "timezone": "auto",
        "forecast_days": 15,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_URL, params=params, timeout=15) as response:
            response.raise_for_status()
            data = await response.json()

    await save_weather_cache(cache_key, data)

    return data
