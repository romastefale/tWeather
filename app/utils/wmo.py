WMO_CODES = {
    0: ("☀️", "Céu limpo"),
    1: ("🌤", "Predominantemente limpo"),
    2: ("⛅️", "Parcialmente nublado"),
    3: ("☁️", "Nublado"),
    45: ("🌫", "Neblina"),
    48: ("🌫", "Neblina intensa"),
    51: ("🌦", "Garoa leve"),
    53: ("🌦", "Garoa moderada"),
    55: ("🌧", "Garoa intensa"),
    61: ("🌦", "Chuva fraca"),
    63: ("🌧", "Chuva moderada"),
    65: ("🌧", "Chuva forte"),
    71: ("❄️", "Neve fraca"),
    73: ("❄️", "Neve moderada"),
    75: ("❄️", "Neve forte"),
    80: ("🌦", "Pancadas de chuva"),
    81: ("🌧", "Pancadas moderadas"),
    82: ("⛈", "Pancadas fortes"),
    95: ("⛈", "Tempestade"),
}


def get_weather_data(code: int):
    return WMO_CODES.get(code, ("🌤", "Tempo variável"))
