import asyncio
import logging

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
logger = logging.getLogger(__name__)

INLINE_RESULTS_LIMIT = 5
INLINE_EMPTY_CACHE = 10
INLINE_RESULTS_CACHE = 60


@router.inline_query()
async def inline_weather(query: InlineQuery):
    text = " ".join(query.query.strip().split())

    if not text:
        await query.answer(
            results=[],
            switch_pm_text='Digite uma cidade para ver a previsão',
            switch_pm_parameter='start',
            cache_time=INLINE_EMPTY_CACHE,
            is_personal=True,
        )
        return

    if len(text) < 3:
        await query.answer(
            results=[],
            switch_pm_text='Digite pelo menos 3 caracteres',
            switch_pm_parameter='start',
            cache_time=INLINE_EMPTY_CACHE,
            is_personal=True,
        )
        return

    try:
        results = await search_location(text)
    except Exception:
        logger.exception('Inline location search failed')
        return

    limited_results = results[:INLINE_RESULTS_LIMIT]

    weather_tasks = [
        get_weather(
            latitude=item["latitude"],
            longitude=item["longitude"],
        )
        for item in limited_results
    ]

    weather_results = await asyncio.gather(
        *weather_tasks,
        return_exceptions=True,
    )

    articles = []

    for index, item in enumerate(limited_results):
        try:
            weather = weather_results[index]

            if isinstance(weather, Exception):
                raise weather

            current = weather["current"]
            daily = weather["daily"]

            _, weather_text = get_weather_data(current['weather_code'])

            message = build_weather_message(item, weather)

            title = f"🌤 {item['name']}"

            if item.get('admin1'):
                title += f", {item['admin1']}"

            description = (
                f"{round(current['temperature_2m'])}°C • "
                f"{weather_text} • "
                f"⬇️ {round(daily['temperature_2m_min'][0])}° "
                f"⬆️ {round(daily['temperature_2m_max'][0])}°"
            )

            article_id = (
                f"{item['latitude']}:"
                f"{item['longitude']}:"
                f"{item['name']}"
            )

            articles.append(
                InlineQueryResultArticle(
                    id=article_id,
                    title=title,
                    description=description,
                    input_message_content=InputTextMessageContent(
                        message_text=message,
                        parse_mode="HTML",
                    ),
                    reply_markup=weather_keyboard(),
                )
            )
        except Exception:
            logger.exception('Inline weather render failed')

    await query.answer(
        articles,
        cache_time=INLINE_RESULTS_CACHE,
        is_personal=True,
    )
