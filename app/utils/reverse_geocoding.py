import aiohttp

REVERSE_URL = "https://geocoding-api.open-meteo.com/v1/reverse"


async def reverse_geocode(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "language": "pt",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(REVERSE_URL, params=params, timeout=10) as response:
            response.raise_for_status()
            data = await response.json()

    results = data.get("results") or []

    if not results:
        return "Localização Atual"

    first = results[0]

    city = first.get("name", "Localização")
    state = first.get("admin1", "")

    return f"{city}, {state}"
