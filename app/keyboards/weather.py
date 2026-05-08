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
                    text="Atualizar",
                    callback_data="weather:refresh",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="3 dias",
                    callback_data="weather:3days",
                ),
                InlineKeyboardButton(
                    text="7 dias",
                    callback_data="weather:7days",
                ),
                InlineKeyboardButton(
                    text="15 dias",
                    callback_data="weather:15days",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Card",
                    callback_data="weather:card",
                ),
                InlineKeyboardButton(
                    text="Trocar cidade",
                    callback_data="weather:change_city",
                ),
            ],
        ]
    )
