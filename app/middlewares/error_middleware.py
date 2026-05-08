from aiogram import BaseMiddleware

from app.utils.logger import get_logger

logger = get_logger(__name__)


class ErrorMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)

        except Exception as error:
            logger.exception('Unhandled error: %s', error)

            message = getattr(event, 'message', None)

            if message:
                try:
                    await message.answer(
                        'Ocorreu um erro temporário. Tente novamente.'
                    )
                except Exception:
                    pass

            return None
