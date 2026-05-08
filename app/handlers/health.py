from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command('healthz'))
async def healthcheck_handler(message: Message):
    await message.answer('OK')
