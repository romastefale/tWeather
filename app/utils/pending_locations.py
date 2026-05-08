import time

PENDING_LOCATIONS = {}
TTL_SECONDS = 600


def set_pending_location(user_id: int, results: list):
    PENDING_LOCATIONS[user_id] = {
        "created_at": time.time(),
        "results": results,
    }



def get_pending_location(user_id: int):
    cleanup_pending_locations()

    data = PENDING_LOCATIONS.get(user_id)

    if not data:
        return None

    return data["results"]



def remove_pending_location(user_id: int):
    PENDING_LOCATIONS.pop(user_id, None)



def cleanup_pending_locations():
    now = time.time()

    expired = []

    for user_id, data in PENDING_LOCATIONS.items():
        if now - data["created_at"] > TTL_SECONDS:
            expired.append(user_id)

    for user_id in expired:
        PENDING_LOCATIONS.pop(user_id, None)
