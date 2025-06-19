# coding utf-8

from aiogram.exceptions import TelegramAPIError

from aiogram.enums.parse_mode import ParseMode

from fastapi.exceptions import HTTPException

from .bot import IBot

from ..core import IConfEnv


class IBotReporter:
    def __init__(
        self,
        conf: IConfEnv,
    ) -> None:
        self._bot = IBot(
            conf,
        )

    async def send_error(
        self,
        error: HTTPException,
        context: str = None,
    ) -> None:
        error_message = (
            f"⚠️ <b>{error.detail}</b> ⚠️\n\n<b>Status:</b> {error.status_code}\n\n"
        )

        if context:
            error_message += f"{context}"

        try:
            await self._bot.telegram_bot.send_message(
                chat_id=self._bot._conf.telegram_chat_id,
                text=error_message,
                parse_mode=ParseMode.HTML,
            )
        except TelegramAPIError as err:
            raise err

    async def send_error_message(
        self,
        error: HTTPException,
        context: str = None,
    ) -> None:
        return await self.send_error(
            error,
            context,
        )
