import asyncio

DEFAULT_RETRIES = 2
DEFAULT_DELAY = 1.0
BACKOFF_MULTIPLIER = 2


async def async_retry(
    function,
    retries: int = DEFAULT_RETRIES,
    delay: float = DEFAULT_DELAY,
):
    last_error = None

    current_delay = delay

    for attempt in range(retries + 1):
        try:
            return await function()

        except Exception as error:
            last_error = error

            if attempt < retries:
                await asyncio.sleep(current_delay)

                current_delay *= BACKOFF_MULTIPLIER

    raise last_error
