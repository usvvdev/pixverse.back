# coding utf-8

from fastapi import UploadFile

from .core import PixVerseCore

from pathlib import Path

from os import path

from ....interface.schemas.api import (
    BaseBody,
    TextBody,
    ImageBody,
    StatusBody,
    ResponseModel,
    UserCredentials,
)

from ....domain.entities.typing.enums import PixVerseUri

from ....domain.entities import (
    TokenHeaders,
    APIHeaders,
    IConfEnv,
)

from ....domain.conf import app_conf


conf: IConfEnv = app_conf()


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

    async def auth_user(
        self,
        body: UserCredentials,
    ) -> ResponseModel:
        return await self._core.post(
            endpoint=PixVerseUri.AUTH,
            body=body,
        )

    async def text_to_video(
        self,
        token: str,
        body: TextBody,
    ) -> ResponseModel:
        return await self._core.post(
            endpoint=PixVerseUri.TEXT,
            headers=TokenHeaders(
                token=token,
            ).dict,
            body=body,
        )

    async def image_to_video(
        self,
        body: BaseBody,
        token: str,
        file: UploadFile,
    ):
        uploaded = await self._core.post(
            endpoint=PixVerseUri.UPLOAD,
            headers=APIHeaders(
                api_key=conf.api_key,
            ).dict,
            files={"image": (file.filename, await file.read(), file.content_type)},
        )
        return await self._core.post(
            endpoint=PixVerseUri.IMAGE,
            headers=TokenHeaders(
                token=token,
            ).dict,
            body=ImageBody(
                **body.dict,
                img_id=uploaded.response.img_id,
                img_url=uploaded.response.img_url,
            ),
        )

    async def generation_status(
        self,
        body: StatusBody,
    ) -> ResponseModel:
        return await self._core.get(
            endpoint=PixVerseUri.STATUS.format(
                id=body.generation_id,
            ),
            headers=APIHeaders(
                api_key=conf.api_key,
            ).dict,
        )
