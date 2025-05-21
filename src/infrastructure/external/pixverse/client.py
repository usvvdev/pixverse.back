# coding utf-8

from typing import Any

from .core import PixVerseCore

from ....interface.schemas.api import (
    TextBody,
    ImageBody,
    StatusBody,
)

from ....domain.entities.typing.enums import PixVerseUri


class PixVerseClient:
    """Клиентский интерфейс для работы с PixVerse API.

    Предоставляет удобные методы для основных операций с видео контентом:
    - Генерация видео из текста
    - Создание видео из изображений
    - Проверка статуса задач

    Args:
        core (PixVerseCore): Базовый клиент для выполнения запросов
    """

    def __init__(
        self,
        core: PixVerseCore,
    ) -> None:
        self._core = core

    async def text_to_video(
        self,
        body: TextBody,
    ) -> dict[str, Any]:
        return await self._core.post(
            endpoint=PixVerseUri.TEXT,
            body=body,
        )

    async def image_to_video(
        self,
        body: ImageBody,
    ) -> dict[str, Any]:
        return await self._core.post(
            endpoint=PixVerseUri.IMAGE,
            body=body,
        )

    async def generation_status(
        self,
        body: StatusBody,
    ) -> dict[str, Any]:
        return await self._core.get(
            endpoint=PixVerseUri.STATUS.format(
                id=body.generation_id,
            ),
        )
