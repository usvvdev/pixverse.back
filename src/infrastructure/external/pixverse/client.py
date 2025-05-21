# coding utf-8

from fastapi import UploadFile

from .core import PixVerseCore

from ....interface.schemas.api import (
    BaseBody,
    TextBody,
    ImageBody,
    StatusBody,
    Resp,
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
    ) -> Resp:
        return await self._core.post(
            endpoint=PixVerseUri.TEXT,
            body=body,
        )

    async def image_to_video(
        self,
        body: BaseBody,
        file: UploadFile,
    ) -> Resp:
        uploaded_response: Resp = await self._core.post(
            endpoint=PixVerseUri.UPLOAD,
            files={"image": (file.filename, await file.read(), file.content_type)},
        )
        return await self._core.post(
            endpoint=PixVerseUri.IMAGE,
            body=ImageBody(
                **body.dict,
                img_id=uploaded_response.res.img_id,
            ),
        )

    async def generation_status(
        self,
        body: StatusBody,
    ) -> Resp:
        return await self._core.get(
            endpoint=PixVerseUri.STATUS.format(
                id=body.generation_id,
            ),
        )
