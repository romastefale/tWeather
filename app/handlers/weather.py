from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, CallbackQuery, Message

from app.keyboards.location_results import multiple_locations_keyboard
from app.keyboards.weather import weather_keyboard
from app.services.card_settings_service import (
    are_cards_enabled,
    set_cards_enabled,
)
from app.services.geocoding_service import search_location
from app.services.location_service import get_user_location, save_user_location
from app.services.weather_service import get_weather
from app.utils.card_cache import (
    get_card_cache,
    get_weather_mode,
    save_card_cache,
    set_weather_mode,
)
from app.utils.pending_locations import (
    get_pending_location,
    remove_pending_location,
    set_pending_location,
)
from app.utils.rate_limit import is_rate_limited
from app.utils.reverse_geocoding import reverse_geocode
from app.utils.telegram import safe_edit_text
from app.utils.weather_card import render_weather_card
from app.utils.weather_formatter import (
    build_multi_day_forecast,
    build_weather_message,
)

router = Router()


async def send_weather_card(message: Message, location, weather, caption=None):
    enabled = await are_cards_enabled(message.chat.id)

    if not enabled:
        return

    try:
        mode = get_weather_mode(message.chat.id)

        weather_code = weather['current']['weather_code']
        temperature = round(weather['current']['temperature_2m'])

        cache_key = (
            f"{location['name']}:{mode}:{weather_code}:{temperature}"
        )

        image_bytes = get_card_cache(cache_key)

        if image_bytes is None:
            image = render_weather_card(location, weather)
            image_bytes = image.read()

            save_card_cache(cache_key, image_bytes)

        await message.answer_photo(
            BufferedInputFile(
                image_bytes,
                filename="weather.png",
            ),
            caption=caption,
            reply_markup=weather_keyboard(),
        )
    except Exception:
        return


@router.message(Command("cards"))
async def cards_handler(message: Message):
    text = message.text.lower().strip()

    if 'off' in text:
        await set_cards_enabled(message.chat.id, False)
        await message.answer('Cards desativados.')
        return

    await set_cards_enabled(message.chat.id, True)
    await message.answer('Cards ativados.')


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

    set_weather_mode(callback.from_user.id, 'today')

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

    if callback.message:
        await send_weather_card(callback.message, location, weather, text)

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

    set_weather_mode(message.chat.id, 'today')

    weather = await get_weather(
        latitude=message.location.latitude,
        longitude=message.location.longitude,
    )

    location = {"name": location_name}

    text = build_weather_message(location, weather)

    await send_weather_card(message, location, weather, text)


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

    set_weather_mode(message.chat.id, 'today')

    weather = await get_weather(
        latitude=location["latitude"],
        longitude=location["longitude"],
    )

    text = build_weather_message(location, weather)

    await send_weather_card(message, location, weather, text)


@router.message()
async def quick_search_handler(message: Message):
    if message.text.startswith("/"):
        return

    if len(message.text.strip()) < 3:
        return

    if is_rate_limited(message.from_user.id):
        return

    results = await search_location(message.text.strip())

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
        force_refresh=action == "refresh",
    )

    if action in ['today', 'refresh']:
        set_weather_mode(callback.from_user.id, 'today')
        text = build_weather_message(location, weather)
    elif action == "3days":
        set_weather_mode(callback.from_user.id, '3days')
        text = build_multi_day_forecast(location, weather, 3)
    elif action == "7days":
        set_weather_mode(callback.from_user.id, '7days')
        text = build_multi_day_forecast(location, weather, 7)
    else:
        set_weather_mode(callback.from_user.id, '15days')
        text = build_multi_day_forecast(location, weather, 15)

    if action == "card":
        mode = get_weather_mode(callback.from_user.id)

        if mode == '3days':
            text = build_multi_day_forecast(location, weather, 3)
        elif mode == '7days':
            text = build_multi_day_forecast(location, weather, 7)
        elif mode == '15days':
            text = build_multi_day_forecast(location, weather, 15)
        else:
            text = build_weather_message(location, weather)

        if callback.message:
            await send_weather_card(callback.message, location, weather, text)

        await callback.answer("Card atualizado")
        return

    if await are_cards_enabled(callback.message.chat.id):
        text += (
            "\n\n🖼 Para atualizar o card visual deste período, "
            "clique no botão Card."
        )

    await safe_edit_text(
        callback,
        text,
        reply_markup=weather_keyboard(),
    )

    await callback.answer("Atualizado")
