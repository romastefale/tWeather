from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from app.keyboards.weather import weather_keyboard
from app.services.geocoding_service import search_location
from app.services.weather_service import get_weather
from app.utils.weather_formatter import build_weather_message
from app.utils.wmo import get_weather_data

router = Router()


@router.inline_query()
async def inline_weather(query: InlineQuery):
    text = query.query.strip()

    if not text:
        await query.answer(
            results=[],
            switch_pm_text='Digite uma cidade para ver a previsão',
            switch_pm_parameter='start',
            cache_time=1,
            is_personal=True,
        )
        return

    results = await search_location(text)

    articles = []

    for index, item in enumerate(results[:5]):
        weather = await get_weather(
            latitude=item["latitude"],
            longitude=item["longitude"],
        )

        current = weather["current"]
        daily = weather["daily"]

        _, weather_text = get_weather_data(current['weather_code'])

        message = build_weather_message(item, weather)

        title = (
            f"🌤 {item['name']}"
        )

        if item.get('admin1'):
            title += f", {item['admin1']}"

        description = (
            f"{round(current['temperature_2m'])}°C • "
            f"{weather_text} • "
            f"⬇️ {round(daily['temperature_2m_min'][0])}° "
            f"⬆️ {round(daily['temperature_2m_max'][0])}°"
        )

        articles.append(
            InlineQueryResultArticle(
                id=str(index),
                title=title,
                description=description,
                input_message_content=InputTextMessageContent(
                    message_text=message,
                    parse_mode="HTML",
                ),
                reply_markup=weather_keyboard(),
            )
        )

    await query.answer(
        articles,
        cache_time=60,
        is_personal=True,
    )
