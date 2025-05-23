# coding utf-8

from fastapi import UploadFile

from .....interface.schemas.api import (
    TextBody,
    BaseBody,
    StatusBody,
    UserCredentials,
)

from .....interface.controllers.api.v1 import PixVerseController

from .....interface.schemas.api import ResponseModel


class PixVerseView:
    def __init__(
        self,
        controller: PixVerseController,
    ) -> None:
        self._controller = controller

    async def auth_user(
        self,
        body: UserCredentials,
    ) -> ResponseModel:
        return await self._controller.auth_user(
            body,
        )

    async def text_to_video(
        self,
        token: str,
        body: TextBody,
    ) -> ResponseModel:
        return await self._controller.text_to_video(
            token,
            body,
        )

    async def image_to_video(
        self,
        body: BaseBody,
        token: str,
        file: UploadFile,
    ):
        return await self._controller.image_to_video(
            body,
            token,
            file,
        )

    async def generation_status(
        self,
        body: StatusBody,
    ) -> ResponseModel:
        return await self._controller.generation_status(
            body,
        )
