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
                    text="Atualizar",
                    callback_data="weather:refresh",
                    style=ButtonStyle.PRIMARY,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="3 dias",
                    callback_data="weather:3days",
                    style=ButtonStyle.SUCCESS,
                ),
                InlineKeyboardButton(
                    text="7 dias",
                    callback_data="weather:7days",
                    style=ButtonStyle.PRIMARY,
                ),
                InlineKeyboardButton(
                    text="15 dias",
                    callback_data="weather:15days",
                    style=ButtonStyle.SUCCESS,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Trocar cidade",
                    callback_data="weather:change_city",
                    style=ButtonStyle.DANGER,
                ),
            ],
        ]
    )
