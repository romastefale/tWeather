from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def weather_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Hoje",
                    callback_data="weather:today",
                ),
                InlineKeyboardButton(
                    text="7 dias",
                    callback_data="weather:7days",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="15 dias",
                    callback_data="weather:15days",
                ),
            ],
        ]
    )
