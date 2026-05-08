import time

RATE_LIMIT = {}
WINDOW_SECONDS = 2



def is_rate_limited(user_id: int) -> bool:
    now = time.time()

    last = RATE_LIMIT.get(user_id)

    if not last:
        RATE_LIMIT[user_id] = now
        return False

    if now - last < WINDOW_SECONDS:
        return True

    RATE_LIMIT[user_id] = now

    return False
