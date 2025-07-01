# coding utf-8

from fastapi import UploadFile

from asyncio import sleep

from .core import CaloriesCore

from base64 import b64encode

from ....domain.conf import app_conf

from ....domain.entities.core import IConfEnv

from ....domain.entities.bot import IBotReporter

from ....domain.entities.chatgpt import CaloriesBody

from ....interface.schemas.external import (
    ChatGPTCaloriesResponse,
    ChatGPTErrorResponse,
    ChatGPTCalories,
    ChatGPTError,
)

from ....domain.errors import CaloriesError

from ....domain.typing.enums import ChatGPTEndpoint


conf: IConfEnv = app_conf()

telegram_bot = IBotReporter(
    conf,
)


class CaloriesClient:
    """Клиентский интерфейс для работы с ChatGPT API.

    Предоставляет удобные методы для основных операций с видео контентом:
    - Генерация видео из текста
    - Создание видео из изображений
    - Проверка статуса задач

    Args:
        core (ChatGPTCore): Базовый клиент для выполнения запросов
    """

    def __init__(
        self,
        core: CaloriesCore,
    ) -> None:
        self._core = core

    async def __handle_failure(
        self,
        last_error: ChatGPTError,
        status_code: int | None = None,
        extra: dict[str] = {},
    ) -> CaloriesError:
        error = CaloriesError(
            status_code=status_code if status_code is not None else 400,
            detail=last_error.message,
            extra=extra,
        )
        raise error

    async def photo_to_calories(
        self,
        image: UploadFile,
    ) -> ChatGPTCalories:
        max_attempts = 10

        last_error = None

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:

                async def call(
                    token: str,
                ) -> ChatGPTCaloriesResponse | ChatGPTErrorResponse:
                    image_bytes = b64encode(await image.read()).decode("utf-8")
                    return await self._core.post(
                        token=token,
                        endpoint=ChatGPTEndpoint.CHAT,
                        body=CaloriesBody.create_image(
                            image_url=f"data:image/jpeg;base64,{image_bytes}"
                        ),
                    )

                data: ChatGPTCaloriesResponse | ChatGPTErrorResponse = await call(token)

                if not isinstance(data, ChatGPTErrorResponse):
                    return data.fetch_data()

                last_error = data.error

            except Exception:
                if attempt == max_attempts - 1:
                    try:
                        data = await call(token)

                        if not data.error:
                            return data.fetch_data()

                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(last_error)
                await sleep(1)
        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    async def text_to_calories(
        self,
        description: str,
    ) -> ChatGPTCalories:
        max_attempts = 10

        last_error = None

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:

                async def call(
                    token: str,
                ) -> ChatGPTCaloriesResponse | ChatGPTErrorResponse:
                    return await self._core.post(
                        token=token,
                        endpoint=ChatGPTEndpoint.CHAT,
                        body=CaloriesBody.create_text(
                            description=description,
                        ),
                    )

                data: ChatGPTCaloriesResponse | ChatGPTErrorResponse = await call(token)

                if not isinstance(data, ChatGPTErrorResponse):
                    return data.fetch_data()

                last_error = data.error

            except Exception:
                if attempt == max_attempts - 1:
                    try:
                        data = await call(token)

                        if not data.error:
                            return data.fetch_data()

                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(last_error)
                await sleep(1)
        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )
