from app.services.cache_service import (
    get_cached_weather,
    save_weather_cache,
)
from app.services.http_client import get_http_session
from app.utils.logger import get_logger
from app.utils.retry import async_retry

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 8
DEFAULT_FORECAST_DAYS = 5

logger = get_logger(__name__)


async def get_weather(
    latitude: float,
    longitude: float,
    force_refresh: bool = False,
    forecast_days: int = DEFAULT_FORECAST_DAYS,
):
    cache_key = (
        f"{round(latitude, 2)}:"
        f"{round(longitude, 2)}:"
        f"{forecast_days}"
    )

    cached = await get_cached_weather(cache_key)

    if cached and not force_refresh:
        logger.info("weather cache hit: %s", cache_key)
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
        "forecast_days": forecast_days,
    }

    async def fetch_weather():
        logger.info(
            "fetching weather lat=%s lon=%s days=%s",
            latitude,
            longitude,
            forecast_days,
        )

        session = await get_http_session()

        async with session.get(
            WEATHER_URL,
            params=params,
            timeout=REQUEST_TIMEOUT,
        ) as response:
            response.raise_for_status()
            return await response.json()

    try:
        data = await async_retry(fetch_weather)

        await save_weather_cache(cache_key, data)

        logger.info("weather updated: %s", cache_key)

        return data

    except Exception as error:
        logger.warning("weather fetch failed: %s", error)

        if cached:
            logger.info("using cached weather fallback: %s", cache_key)
            return cached

        raise
