import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from app.database import init_db
from app.handlers.start import router as start_router
from app.handlers.weather import router as weather_router

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    logging.basicConfig(level=logging.INFO)

    await init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(weather_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
