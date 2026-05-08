import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

logger = logging.getLogger(__name__)

MAX_TEXT_LENGTH = 4000


async def safe_edit_text(
    callback: CallbackQuery,
    text: str,
    reply_markup=None,
):
    try:
        text = text[:MAX_TEXT_LENGTH]

        if callback.inline_message_id:
            await callback.bot.edit_message_text(
                inline_message_id=callback.inline_message_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode="HTML",
                disable_web_page_preview=True,
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
            disable_web_page_preview=True,
        )

    except TelegramBadRequest as error:
        error_text = str(error).lower()

        ignored_errors = [
            "message is not modified",
            "message to edit not found",
            "query is too old",
            "message can't be edited",
            "there is no text in the message to edit",
        ]

        for ignored_error in ignored_errors:
            if ignored_error in error_text:
                logger.warning(
                    "Ignored Telegram edit issue: %s",
                    ignored_error,
                )
                return

        logger.exception("Telegram edit failed")

    except Exception:
        logger.exception("safe_edit_text failed")
