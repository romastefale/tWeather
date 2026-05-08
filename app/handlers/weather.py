from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.keyboards.location_results import multiple_locations_keyboard
from app.keyboards.weather import weather_keyboard
from app.services.geocoding_service import search_location
from app.services.location_service import get_user_location, save_user_location
from app.services.weather_service import get_weather
from app.utils.weather_formatter import (
    build_multi_day_forecast,
    build_weather_message,
)

router = Router()

PENDING_LOCATIONS = {}


@router.message(Command("buscar"))
async def buscar_handler(message: Message):
    query = message.text.replace("/buscar", "").strip()

    if not query:
        await message.answer("Envie uma cidade. Exemplo: /buscar Rio de Janeiro")
        return

    results = await search_location(query)

    if not results:
        await message.answer("Nenhum local encontrado.")
        return

    PENDING_LOCATIONS[message.from_user.id] = results

    await message.answer(
        "📍 Selecione o local desejado:",
        reply_markup=multiple_locations_keyboard(results),
    )


@router.callback_query(F.data.startswith("pick_location:"))
async def pick_location_callback(callback: CallbackQuery):
    results = PENDING_LOCATIONS.get(callback.from_user.id)

    if not results:
        await callback.answer("Busca expirada", show_alert=True)
        return

    index = int(callback.data.split(":")[1])

    if index >= len(results):
        await callback.answer("Local inválido", show_alert=True)
        return

    location = results[index]

    await save_user_location(
        user_id=callback.from_user.id,
        name=location["name"],
        country=location.get("country"),
        admin1=location.get("admin1"),
        latitude=location["latitude"],
        longitude=location["longitude"],
    )

    weather = await get_weather(
        latitude=location["latitude"],
        longitude=location["longitude"],
    )

    text = build_weather_message(location, weather)

    await callback.message.edit_text(
        text,
        reply_markup=weather_keyboard(),
    )

    await callback.answer("Local selecionado")


@router.callback_query(F.data == "cancel_location")
async def cancel_location_callback(callback: CallbackQuery):
    PENDING_LOCATIONS.pop(callback.from_user.id, None)

    await callback.message.edit_text("Busca cancelada.")

    await callback.answer("Cancelado")


@router.message(F.location)
async def location_handler(message: Message):
    await save_user_location(
        user_id=message.from_user.id,
        name="Localização Atual",
        latitude=message.location.latitude,
        longitude=message.location.longitude,
    )

    weather = await get_weather(
        latitude=message.location.latitude,
        longitude=message.location.longitude,
    )

    text = build_weather_message(
        {"name": "Localização Atual"},
        weather,
    )

    await message.answer(
        text,
        reply_markup=weather_keyboard(),
    )


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


@router.message()
async def quick_search_handler(message: Message):
    if message.text.startswith("/"):
        return

    results = await search_location(message.text.strip())

    if not results:
        return

    PENDING_LOCATIONS[message.from_user.id] = results

    await message.answer(
        "📍 Selecione o local desejado:",
        reply_markup=multiple_locations_keyboard(results),
    )


@router.callback_query(F.data.startswith("weather:"))
async def weather_callback(callback: CallbackQuery):
    action = callback.data.split(":")[1]

    if action == "change_city":
        await callback.message.edit_text(
            "📍 Envie o nome de uma cidade para trocar o local.")

        await callback.answer("Trocar cidade")
        return

    location = await get_user_location(callback.from_user.id)

    if not location:
        await callback.answer("Local não encontrado", show_alert=True)
        return

    weather = await get_weather(
        latitude=location["latitude"],
        longitude=location["longitude"],
    )

    if action == "today":
        text = build_weather_message(location, weather)
    elif action == "3days":
        text = build_multi_day_forecast(location, weather, 3)
    elif action == "7days":
        text = build_multi_day_forecast(location, weather, 7)
    else:
        text = build_multi_day_forecast(location, weather, 15)

    await callback.message.edit_text(
        text,
        reply_markup=weather_keyboard(),
    )

    await callback.answer("Atualizado")
