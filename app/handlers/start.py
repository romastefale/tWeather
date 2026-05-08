from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    text = (
        "🌤 <b>tWeather</b>\n\n"
        "Previsão do tempo rápida e leve.\n\n"
        "Envie uma cidade, localização ou use:\n\n"
        "• /tempo\n"
        "• /buscar Rio de Janeiro\n"
        "• /help"
    )

    await message.answer(text)


@router.message(Command("help"))
async def help_handler(message: Message):
    text = (
        "📘 <b>Comandos disponíveis</b>\n\n"
        "• /tempo → mostra previsão do local salvo\n"
        "• /buscar cidade → procurar cidade\n"
        "• /help → ver ajuda\n\n"
        "Você também pode:\n"
        "• enviar uma localização\n"
        "• digitar apenas o nome da cidade\n"
        "• usar inline mode:\n"
        "@tigraoWeatherbot rio"
    )

    await message.answer(text)
