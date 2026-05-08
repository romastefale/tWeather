from datetime import datetime
from zoneinfo import ZoneInfo

from app.utils.alerts import build_weather_alerts
from app.utils.day_periods import build_day_periods
from app.utils.wmo import get_weather_data

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



def format_ptbr_date(date_string: str) -> str:
    date = datetime.strptime(date_string, "%Y-%m-%d")

    weekday = WEEKDAYS[date.weekday()]
    month = MONTHS[date.month - 1]

    return f"{weekday}, {date.day} de {month}"



def build_temperature_text(min_temp: int, max_temp: int):
    if max_temp >= 32:
        return "Calor mais intenso durante a tarde."

    if min_temp <= 10:
        return "Amanhecer com temperaturas mais frias."

    return "Temperatura estável ao longo do dia."



def build_updated_time():
    now = datetime.now(ZoneInfo("America/Sao_Paulo"))

    return now.strftime("%H:%M")



def build_weather_message(location, weather):
    current = weather["current"]
    daily = weather["daily"]
    hourly = weather["hourly"]

    emoji, weather_text = get_weather_data(current["weather_code"])

    periods = build_day_periods(hourly)

    alerts = build_weather_alerts(weather)

    updated_at = build_updated_time()

    alerts_block = f"{alerts}\n\n" if alerts else ""

    return (
        f"{emoji} <b>{location['name']}</b>\n\n"
        f"{weather_text}.\n"
        f"{build_temperature_text(round(daily['temperature_2m_min'][0]), round(daily['temperature_2m_max'][0]))}\n\n"
        f"<b>{round(current['temperature_2m'])}°C agora"
        f" • Sensação {round(current['apparent_temperature'])}°C</b>\n\n"
        f"⬇️ {round(daily['temperature_2m_min'][0])}°"
        f" • ⬆️ {round(daily['temperature_2m_max'][0])}°"
        f" • ☔ {daily['precipitation_probability_max'][0]}%\n\n"
        f"{alerts_block}"
        f"{periods}\n\n"
        f"<i>Atualizado às {updated_at}</i>"
    )



def build_multi_day_forecast(location, weather, days: int):
    daily = weather['daily']
    dates = daily['time']
    min_temp = daily['temperature_2m_min']
    max_temp = daily['temperature_2m_max']
    rain = daily['precipitation_probability_max']
    codes = daily['weather_code']

    updated_at = build_updated_time()

    lines = [f"🌤 <b>{location['name']}</b>\n"]

    for index in range(days):
        emoji, weather_text = get_weather_data(codes[index])

        formatted_date = format_ptbr_date(dates[index])

        lines.append(
            (
                f"{emoji} <b>{formatted_date}</b>\n\n"
                f"{weather_text}.\n"
                f"{build_temperature_text(round(min_temp[index]), round(max_temp[index]))}\n\n"
                f"<b>⬇️ {round(min_temp[index])}°"
                f" • ⬆️ {round(max_temp[index])}°"
                f" • ☔ {rain[index]}%</b>\n"
            )
        )

    lines.append(f"\n<i>Atualizado às {updated_at}</i>")

    return "\n".join(lines)
