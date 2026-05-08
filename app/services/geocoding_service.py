from app.services.http_client import get_http_session

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
REQUEST_TIMEOUT = 8


async def search_location(query: str, count: int = 5):
    params = {
        "name": query,
        "count": count,
        "language": "pt",
        "format": "json",
    }

    session = await get_http_session()

    async with session.get(
        GEOCODING_URL,
        params=params,
        timeout=REQUEST_TIMEOUT,
    ) as response:
        response.raise_for_status()

        data = await response.json()

        return data.get("results", [])
