USER_WEATHER_STATE = {}



def set_weather_mode(user_id: int, mode: str):
    current = USER_WEATHER_STATE.get(user_id, {})

    current['mode'] = mode

    USER_WEATHER_STATE[user_id] = current



def get_weather_mode(user_id: int):
    state = USER_WEATHER_STATE.get(user_id)

    if not state:
        return 'today'

    return state.get('mode', 'today')
