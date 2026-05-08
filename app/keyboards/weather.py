from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def weather_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Hoje",
                    callback_data="weather:today",
                    style=ButtonStyle.PRIMARY,
                ),
                InlineKeyboardButton(
                    text="7 dias",
                    callback_data="weather:7days",
                    style=ButtonStyle.SUCCESS,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="15 dias",
                    callback_data="weather:15days",
                    style=ButtonStyle.DANGER,
                ),
            ],
        ]
    )
