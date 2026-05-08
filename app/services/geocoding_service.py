import aiohttp

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


async def search_location(query: str, count: int = 5):
    params = {
        "name": query,
        "count": count,
        "language": "pt",
        "format": "json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(GEOCODING_URL, params=params) as response:
            data = await response.json()
            return data.get("results", [])
