# coding utf-8

from fastapi import UploadFile

from .....interface.schemas.api import (
    TextBody,
    BaseBody,
    StatusBody,
)

from .....interface.controllers.api.v1 import PixVerseController

from .....interface.schemas.api import Resp


class PixVerseView:
    def __init__(
        self,
        controller: PixVerseController,
    ) -> None:
        self._controller = controller

    async def text_to_video(
        self,
        body: TextBody,
    ) -> Resp:
        return await self._controller.text_to_video(
            body,
        )

    async def image_to_video(
        self,
        body: BaseBody,
        file: UploadFile,
    ) -> Resp:
        return await self._controller.image_to_video(
            body,
            file,
        )

    async def generation_status(
        self,
        body: StatusBody,
    ) -> Resp:
        return await self._controller.generation_status(
            body,
        )
