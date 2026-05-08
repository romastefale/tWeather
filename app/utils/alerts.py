def build_weather_alerts(weather):
    daily = weather["daily"]

    alerts = []

    rain = daily["precipitation_probability_max"]
    max_temp = daily["temperature_2m_max"]
    min_temp = daily["temperature_2m_min"]

    if rain[0] >= 80:
        alerts.append("⚠️ Alta chance de chuva hoje.")

    if max_temp[0] >= 35:
        alerts.append("🥵 Calor intenso previsto para hoje.")

    if min_temp[0] <= 5:
        alerts.append("🥶 Temperaturas muito baixas durante a madrugada.")

    if rain[1] >= 80:
        alerts.append("🌧 Chuva forte prevista para amanhã.")

    return "\n".join(alerts)
