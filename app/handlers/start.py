from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    text = (
        "🌤 <b>tWeather</b>\n\n"
        "Previsão do tempo rápida, leve e organizada.\n\n"
        "• Open-Meteo\n"
        "• Inline mode\n"
        "• Localização Telegram\n"
        "• Previsão até 15 dias\n\n"
        "Envie uma cidade, compartilhe localização ou use:\n\n"
        "• /tempo\n"
        "• /buscar Rio de Janeiro\n"
        "• /help"
    )

    await message.answer(text)


@router.message(Command("help"))
async def help_handler(message: Message):
    text = (
        "📘 <b>Comandos disponíveis</b>\n\n"
        "• /tempo → previsão do local salvo\n"
        "• /buscar cidade → procurar cidade\n"
        "• /healthz → verificar status\n"
        "• /help → ver ajuda\n\n"
        "Recursos:\n"
        "• previsão de hoje\n"
        "• previsão 3, 7 e 15 dias\n"
        "• troca rápida de cidade\n"
        "• local salvo por usuário\n"
        "• localização Telegram\n"
        "• inline mode\n\n"
        "Inline:\n"
        "@tigraoWeatherbot rio"
    )

    await message.answer(text)
