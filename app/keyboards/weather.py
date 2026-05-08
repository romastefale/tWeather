from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def weather_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Hoje",
                    callback_data="weather:today",
                    style="primary",
                ),
                InlineKeyboardButton(
                    text="Atualizar",
                    callback_data="weather:refresh",
                    style="primary",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="3 dias",
                    callback_data="weather:3days",
                    style="success",
                ),
                InlineKeyboardButton(
                    text="7 dias",
                    callback_data="weather:7days",
                    style="primary",
                ),
                InlineKeyboardButton(
                    text="15 dias",
                    callback_data="weather:15days",
                    style="success",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Trocar cidade",
                    callback_data="weather:change_city",
                    style="danger",
                ),
            ],
        ]
    )
