from datetime import datetime

WEEKDAYS = [
    "Segunda",
    "Terça",
    "Quarta",
    "Quinta",
    "Sexta",
    "Sábado",
    "Domingo",
]

MONTHS = [
    "janeiro",
    "fevereiro",
    "março",
    "abril",
    "maio",
    "junho",
    "julho",
    "agosto",
    "setembro",
    "outubro",
    "novembro",
    "dezembro",
]


def get_period_name(hour: int) -> str:
    if 0 <= hour < 6:
        return "🌃 Madrugada"
    if 6 <= hour < 12:
        return "🌅 Manhã"
    if 12 <= hour < 18:
        return "☀️ Tarde"
    return "🌙 Noite"


def get_weather_emoji(rain_probability: int) -> str:
    if rain_probability >= 80:
        return "⛈"
    if rain_probability >= 50:
        return "🌧"
    if rain_probability >= 20:
        return "🌦"
    return "☀️"


def format_ptbr_date(date_string: str) -> str:
    date = datetime.strptime(date_string, "%Y-%m-%d")

    weekday = WEEKDAYS[date.weekday()]
    month = MONTHS[date.month - 1]

    return f"{weekday}, {date.day} de {month}"


def build_weather_message(location, weather):
    current = weather["current"]
    daily = weather["daily"]

    return (
        f"🌤 <b>{location['name']}</b>\n\n"
        f"Agora: {round(current['temperature_2m'])}°C\n"
        f"Sensação: {round(current['apparent_temperature'])}°C\n"
        f"💨 {round(current['wind_speed_10m'])} km/h\n"
        f"💧 {current['relative_humidity_2m']}%\n\n"
        f"Hoje\n"
        f"⬇️ {round(daily['temperature_2m_min'][0])}°"
        f" ⬆️ {round(daily['temperature_2m_max'][0])}°\n\n"
        f"☔ Chance de chuva: {daily['precipitation_probability_max'][0]}%"
    )


def build_multi_day_forecast(location, weather, days: int):
    daily = weather["daily"]
    dates = daily["time"]
    min_temp = daily["temperature_2m_min"]
    max_temp = daily["temperature_2m_max"]
    rain = daily["precipitation_probability_max"]

    lines = [f"🌤 <b>{location['name']}</b>\n"]

    for index in range(days):
        emoji = get_weather_emoji(rain[index])
        formatted_date = format_ptbr_date(dates[index])

        lines.append(
            (
                f"{emoji} <b>{formatted_date}</b>\n"
                f"⬇️ {round(min_temp[index])}°"
                f" ⬆️ {round(max_temp[index])}°\n"
                f"☔ {rain[index]}%\n"
            )
        )

    return "\n".join(lines)
