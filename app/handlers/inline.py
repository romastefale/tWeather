from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from app.services.geocoding_service import search_location
from app.services.weather_service import get_weather
from app.utils.weather_formatter import build_weather_message

router = Router()


@router.inline_query()
async def inline_weather(query: InlineQuery):
    text = query.query.strip()

    if not text:
        return

    results = await search_location(text)

    articles = []

    for index, item in enumerate(results[:5]):
        weather = await get_weather(
            latitude=item["latitude"],
            longitude=item["longitude"],
        )

        message = build_weather_message(item, weather)

        articles.append(
            InlineQueryResultArticle(
                id=str(index),
                title=f"{item['name']} - {item.get('country', '')}",
                description="Previsão do tempo",
                input_message_content=InputTextMessageContent(
                    message_text=message,
                    parse_mode="HTML",
                ),
            )
        )

    await query.answer(
        articles,
        cache_time=60,
        is_personal=True,
    )
