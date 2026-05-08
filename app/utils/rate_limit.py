import time

RATE_LIMIT = {}
WINDOW_SECONDS = 2
MAX_TRACKED_USERS = 5000



def cleanup_rate_limit(now: float):
    if len(RATE_LIMIT) < MAX_TRACKED_USERS:
        return

    expired = []

    for user_id, timestamp in RATE_LIMIT.items():
        if now - timestamp > WINDOW_SECONDS * 10:
            expired.append(user_id)

    for user_id in expired:
        RATE_LIMIT.pop(user_id, None)



def is_rate_limited(user_id: int) -> bool:
    now = time.time()

    cleanup_rate_limit(now)

    last = RATE_LIMIT.get(user_id)

    if not last:
        RATE_LIMIT[user_id] = now
        return False

    if now - last < WINDOW_SECONDS:
        return True

    RATE_LIMIT[user_id] = now

    return False
