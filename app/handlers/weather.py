import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.keyboards.location_results import multiple_locations_keyboard
from app.keyboards.weather import weather_keyboard
from app.services.geocoding_service import search_location
from app.services.location_service import get_user_location, save_user_location
from app.services.weather_service import get_weather
from app.utils.card_cache import get_weather_mode, set_weather_mode
from app.utils.pending_locations import (
    get_pending_location,
    remove_pending_location,
    set_pending_location,
)
from app.utils.rate_limit import is_rate_limited
from app.utils.reverse_geocoding import reverse_geocode
from app.utils.telegram import safe_edit_text
from app.utils.weather_formatter import (
    build_multi_day_forecast,
    build_weather_message,
)

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("buscar"))
async def buscar_handler(message: Message):
    if is_rate_limited(message.from_user.id):
        return

    query = message.text.replace("/buscar", "").strip()

    if not query:
        await message.answer("Envie uma cidade. Exemplo: /buscar Rio de Janeiro")
        return

    results = await search_location(query)

    if not results:
        await message.answer("Nenhum local encontrado.")
        return

    set_pending_location(message.from_user.id, results)

    await message.answer(
        "📍 Selecione o local desejado:",
        reply_markup=multiple_locations_keyboard(results),
    )


@router.callback_query(F.data.startswith("pick_location:"))
async def pick_location_callback(callback: CallbackQuery):
    results = get_pending_location(callback.from_user.id)

    if not results:
        await callback.answer("Busca expirada", show_alert=True)
        return

    index = int(callback.data.split(":")[1])

    if index >= len(results):
        await callback.answer("Local inválido", show_alert=True)
        return

    location = results[index]

    remove_pending_location(callback.from_user.id)

    await save_user_location(
        user_id=callback.from_user.id,
        name=location["name"],
        country=location.get("country"),
        admin1=location.get("admin1"),
        latitude=location["latitude"],
        longitude=location["longitude"],
    )

    set_weather_mode(callback.from_user.id, "today")

    weather = await get_weather(
        latitude=location["latitude"],
        longitude=location["longitude"],
    )

    text = build_weather_message(location, weather)

    await safe_edit_text(
        callback,
        text,
        reply_markup=weather_keyboard(),
    )

    await callback.answer("Local selecionado")


@router.callback_query(F.data == "cancel_location")
async def cancel_location_callback(callback: CallbackQuery):
    remove_pending_location(callback.from_user.id)

    await safe_edit_text(callback, "Busca cancelada.")

    await callback.answer("Cancelado")


@router.message(F.location)
async def location_handler(message: Message):
    if is_rate_limited(message.from_user.id):
        return

    location_name = await reverse_geocode(
        message.location.latitude,
        message.location.longitude,
    )

    await save_user_location(
        user_id=message.from_user.id,
        name=location_name,
        latitude=message.location.latitude,
        longitude=message.location.longitude,
    )

    set_weather_mode(message.from_user.id, "today")

    weather = await get_weather(
        latitude=message.location.latitude,
        longitude=message.location.longitude,
    )

    location = {"name": location_name}

    text = build_weather_message(location, weather)

    await message.answer(
        text,
        reply_markup=weather_keyboard(),
    )


@router.message(Command("tempo"))
async def tempo_handler(message: Message):
    if is_rate_limited(message.from_user.id):
        return

    location = await get_user_location(message.from_user.id)

    if not location:
        await message.answer(
            "Você ainda não possui local salvo. Use /buscar cidade"
        )
        return

    set_weather_mode(message.from_user.id, "today")

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
    if not message.text:
        return

    if message.text.startswith("/"):
        return

    query = message.text.strip()

    if len(query) < 3:
        return

    if is_rate_limited(message.from_user.id):
        return

    results = await search_location(query)

    if not results:
        return

    set_pending_location(message.from_user.id, results)

    await message.answer(
        "📍 Selecione o local desejado:",
        reply_markup=multiple_locations_keyboard(results),
    )


@router.callback_query(F.data.startswith("weather:"))
async def weather_callback(callback: CallbackQuery):
    action = callback.data.split(":")[1]

    if action == "change_city":
        await safe_edit_text(
            callback,
            "📍 Envie o nome de uma cidade para trocar o local.",
        )

        await callback.answer("Trocar cidade")
        return

    location = await get_user_location(callback.from_user.id)

    if not location:
        await callback.answer("Local não encontrado", show_alert=True)
        return

    weather = await get_weather(
        latitude=location["latitude"],
        longitude=location["longitude"],
        force_refresh=action == "refresh",
    )

    current_mode = get_weather_mode(callback.from_user.id)

    if action == "refresh":
        action = current_mode

    if action == "today":
        set_weather_mode(callback.from_user.id, "today")
        text = build_weather_message(location, weather)
    elif action == "3days":
        set_weather_mode(callback.from_user.id, "3days")
        text = build_multi_day_forecast(location, weather, 3)
    elif action == "7days":
        set_weather_mode(callback.from_user.id, "7days")
        text = build_multi_day_forecast(location, weather, 7)
    elif action == "15days":
        set_weather_mode(callback.from_user.id, "15days")
        text = build_multi_day_forecast(location, weather, 15)
    else:
        set_weather_mode(callback.from_user.id, "today")
        text = build_weather_message(location, weather)

    await safe_edit_text(
        callback,
        text,
        reply_markup=weather_keyboard(),
    )

    await callback.answer("Atualizado")
