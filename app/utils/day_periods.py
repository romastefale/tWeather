from app.utils.wmo import get_weather_data



def build_day_periods(hourly):
    periods = {
        "🌅 Manhã": None,
        "☀️ Tarde": None,
        "🌙 Noite": None,
    }

    times = hourly["time"]
    codes = hourly["weather_code"]

    for index, time_string in enumerate(times[:24]):
        hour = int(time_string.split("T")[1].split(":")[0])

        weather = get_weather_data(codes[index])

        if 6 <= hour < 12 and periods["🌅 Manhã"] is None:
            periods["🌅 Manhã"] = weather

        elif 12 <= hour < 18 and periods["☀️ Tarde"] is None:
            periods["☀️ Tarde"] = weather

        elif 18 <= hour < 24 and periods["🌙 Noite"] is None:
            periods["🌙 Noite"] = weather

    lines = []

    for period_name, data in periods.items():
        if not data:
            continue

        emoji, text = data

        lines.append(
            f"{period_name} • {emoji} {text}."
        )

    if not lines:
        return ""

    return "<blockquote>" + "\n".join(lines) + "</blockquote>"
