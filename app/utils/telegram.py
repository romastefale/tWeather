from aiogram.types import CallbackQuery


async def safe_edit_text(
    callback: CallbackQuery,
    text: str,
    reply_markup=None,
):
    try:
        if callback.inline_message_id:
            await callback.bot.edit_message_text(
                inline_message_id=callback.inline_message_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode="HTML",
            )
        else:
            await callback.message.edit_text(
                text,
                reply_markup=reply_markup,
            )
    except Exception:
        pass
