from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def multiple_locations_keyboard(results: list):
    rows = []

    for index, item in enumerate(results[:5]):
        state = item.get("admin1", "")
        country = item.get("country", "")

        rows.append(
            [
                InlineKeyboardButton(
                    text=f"{item['name']}, {state}",
                    callback_data=f"pick_location:{index}",
                    style=ButtonStyle.PRIMARY,
                )
            ]
        )

    rows.append(
        [
            InlineKeyboardButton(
                text="Cancelar",
                callback_data="cancel_location",
                style=ButtonStyle.DANGER,
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=rows)
