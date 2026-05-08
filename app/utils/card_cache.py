import time

CARD_CACHE = {}
TTL_SECONDS = 600

USER_WEATHER_STATE = {}



def set_weather_mode(user_id: int, mode: str):
    USER_WEATHER_STATE[user_id] = {
        'mode': mode,
    }



def get_weather_mode(user_id: int):
    state = USER_WEATHER_STATE.get(user_id)

    if not state:
        return 'today'

    return state.get('mode', 'today')



def get_card_cache(key: str):
    item = CARD_CACHE.get(key)

    if not item:
        return None

    created_at = item['created_at']

    if time.time() - created_at > TTL_SECONDS:
        CARD_CACHE.pop(key, None)
        return None

    return item['data']



def save_card_cache(key: str, data):
    CARD_CACHE[key] = {
        'created_at': time.time(),
        'data': data,
    }



def cleanup_card_cache():
    now = time.time()

    expired = []

    for key, item in CARD_CACHE.items():
        if now - item['created_at'] > TTL_SECONDS:
            expired.append(key)

    for key in expired:
        CARD_CACHE.pop(key, None)
