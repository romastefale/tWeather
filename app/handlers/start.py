from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    text = (
        "🌤 <b>tWeather</b>\n\n"
        "Previsão do tempo rápida e leve.\n\n"
        "Envie uma cidade, localização ou use:\n\n"
        "• /tempo\n"
        "• /buscar Rio de Janeiro"
    )

    await message.answer(text)
