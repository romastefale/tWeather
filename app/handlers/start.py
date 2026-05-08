from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    text = (
        "🌤 <b>tWeather</b>\n\n"
        "Envie uma cidade, localização ou use:\n"
        "/tempo\n"
        "/buscar sorocaba"
    )

    await message.answer(text)
