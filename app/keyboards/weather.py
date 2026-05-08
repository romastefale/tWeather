from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def weather_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Hoje",
                    callback_data="weather:today",
                    extra_data={"style": "primary"},
                ),
                InlineKeyboardButton(
                    text="7 dias",
                    callback_data="weather:7days",
                    extra_data={"style": "positive"},
                ),
            ],
            [
                InlineKeyboardButton(
                    text="15 dias",
                    callback_data="weather:15days",
                    extra_data={"style": "secondary"},
                ),
            ],
        ]
    )
