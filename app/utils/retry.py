import asyncio


async def async_retry(function, retries: int = 2, delay: float = 1.0):
    last_error = None

    for attempt in range(retries + 1):
        try:
            return await function()

        except Exception as error:
            last_error = error

            if attempt < retries:
                await asyncio.sleep(delay)

    raise last_error
