# coding utf-8

from fastapi import UploadFile

from .core import CaloriesCore

from base64 import b64encode

from ....domain.conf import app_conf

from ....domain.entities.core import IConfEnv

from ....domain.entities.chatgpt import CaloriesBody

from ....domain.typing.enums import ChatGPTEndpoint

conf: IConfEnv = app_conf()


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

    async def photo_to_calories(
        self,
        image: UploadFile,
    ):
        image_bytes = b64encode(await image.read()).decode("utf-8")
        response = await self._core.post(
            endpoint=ChatGPTEndpoint.CHAT,
            body=CaloriesBody.create_image(
                image_url=f"data:image/jpeg;base64,{image_bytes}"
            ),
        )
        return response["choices"][0]["message"]["content"]

    async def text_to_calories(
        self,
        description: str,
    ):
        response = await self._core.post(
            endpoint=ChatGPTEndpoint.CHAT,
            body=CaloriesBody.create_text(
                description=description,
            ),
        )
        return response["choices"][0]["message"]["content"]
