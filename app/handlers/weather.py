from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.keyboards.weather import weather_keyboard
from app.services.geocoding_service import search_location
from app.services.location_service import get_user_location, save_user_location
from app.services.weather_service import get_weather
from app.utils.weather_formatter import (
    build_multi_day_forecast,
    build_weather_message,
)

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

    await message.answer(f"📍 Local salvo: {first['name']}")


@router.message(F.location)
async def location_handler(message: Message):
    await save_user_location(
        user_id=message.from_user.id,
        name="Localização Atual",
        latitude=message.location.latitude,
        longitude=message.location.longitude,
    )

    await message.answer("📍 Localização salva com sucesso.")


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

    text = build_weather_message(location, weather)

    await message.answer(
        text,
        reply_markup=weather_keyboard(),
    )


@router.callback_query(F.data.startswith("weather:"))
async def weather_callback(callback: CallbackQuery):
    location = await get_user_location(callback.from_user.id)

    if not location:
        await callback.answer("Local não encontrado", show_alert=True)
        return

    weather = await get_weather(
        latitude=location["latitude"],
        longitude=location["longitude"],
    )

    action = callback.data.split(":")[1]

    if action == "today":
        text = build_weather_message(location, weather)
    elif action == "7days":
        text = build_multi_day_forecast(location, weather, 7)
    else:
        text = build_multi_day_forecast(location, weather, 15)

    await callback.message.edit_text(
        text,
        reply_markup=weather_keyboard(),
    )

    await callback.answer("Atualizado")
