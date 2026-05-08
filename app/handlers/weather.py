from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.geocoding_service import search_location
from app.services.location_service import get_user_location, save_user_location
from app.services.weather_service import get_weather

router = Router()


@router.message(Command("buscar"))
async def buscar_handler(message: Message):
    query = message.text.replace("/buscar", "").strip()

    if not query:
        await message.answer("Envie uma cidade. Exemplo: /buscar Sorocaba")
        return

    results = await search_location(query)

    if not results:
        await message.answer("Nenhum local encontrado.")
        return

    first = results[0]

    await save_user_location(
        user_id=message.from_user.id,
        name=first["name"],
        country=first.get("country"),
        admin1=first.get("admin1"),
        latitude=first["latitude"],
        longitude=first["longitude"],
    )

    text = (
        f"📍 Local salvo: {first['name']}"
    )

    await message.answer(text)


@router.message(Command("tempo"))
async def tempo_handler(message: Message):
    location = await get_user_location(message.from_user.id)

    if not location:
        await message.answer(
            "Você ainda não possui local salvo. Use /buscar cidade"
        )
        return

    weather = await get_weather(
        latitude=location["latitude"],
        longitude=location["longitude"],
    )

    current = weather["current"]
    daily = weather["daily"]

    text = (
        f"🌤 <b>{location['name']}</b>\n\n"
        f"Agora: {round(current['temperature_2m'])}°C\n"
        f"Sensação: {round(current['apparent_temperature'])}°C\n"
        f"💨 {round(current['wind_speed_10m'])} km/h\n"
        f"💧 {current['relative_humidity_2m']}%\n\n"
        f"Hoje\n"
        f"⬇️ {round(daily['temperature_2m_min'][0])}°"
        f" ⬆️ {round(daily['temperature_2m_max'][0])}°"
    )

    await message.answer(text)
