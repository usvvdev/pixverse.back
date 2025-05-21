# coding utf-8

from fastapi import UploadFile

from ....schemas.api import (
    BaseBody,
    TextBody,
    StatusBody,
)

from .....infrastructure.external.pixverse import PixVerseClient

from .....interface.schemas.api import Resp


class PixVerseController:
    def __init__(
        self,
        client: PixVerseClient,
    ) -> None:
        self._client = client

    async def text_to_video(
        self,
        body: TextBody,
    ) -> Resp:
        return await self._client.text_to_video(
            body,
        )

    async def image_to_video(
        self,
        body: BaseBody,
        file: UploadFile,
    ) -> Resp:
        return await self._client.image_to_video(
            body,
            file,
        )

    async def generation_status(
        self,
        body: StatusBody,
    ) -> Resp:
        return await self._client.generation_status(
            body,
        )
