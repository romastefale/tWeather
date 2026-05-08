from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirm_location_keyboard(index: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Confirmar",
                    callback_data=f"confirm_location:{index}",
                ),
                InlineKeyboardButton(
                    text="❌ Cancelar",
                    callback_data="cancel_location",
                ),
            ]
        ]
    )
