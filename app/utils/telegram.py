import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

logger = logging.getLogger(__name__)


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
            return

        if not callback.message:
            return

        current_text = callback.message.text or callback.message.caption

        if current_text == text:
            return

        await callback.message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )

    except TelegramBadRequest as error:
        error_text = str(error).lower()

        if "message is not modified" in error_text:
            return

        if "message to edit not found" in error_text:
            return

        if "query is too old" in error_text:
            return

        logger.exception("Telegram edit failed")

    except Exception:
        logger.exception("safe_edit_text failed")
