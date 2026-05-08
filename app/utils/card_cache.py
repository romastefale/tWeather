CARD_CACHE = {}



def get_card_cache(key: str):
    return CARD_CACHE.get(key)



def save_card_cache(key: str, data):
    CARD_CACHE[key] = data
