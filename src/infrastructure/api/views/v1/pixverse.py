# coding utf-8

from fastapi import UploadFile

from fastapi.security import OAuth2PasswordRequestForm

from .....domain.entities import IBody

from .....interface.controllers.api.v1 import PixVerseController

from .....interface.schemas.api import (
    StatusBody,
    ResponseModel,
)


class PixVerseView:
    def __init__(
        self,
        controller: PixVerseController,
    ) -> None:
        self._controller = controller

    async def auth_user(
        self,
        body: OAuth2PasswordRequestForm,
    ) -> ResponseModel:
        return await self._controller.auth_user(
            body,
        )

    async def text_to_video(
        self,
        token: str,
        body: IBody,
    ) -> ResponseModel:
        return await self._controller.text_to_video(
            token,
            body,
        )

    async def image_to_video(
        self,
        token: str,
        body: IBody,
        file: UploadFile,
    ) -> ResponseModel:
        return await self._controller.image_to_video(
            token,
            body,
            file,
        )

    async def generation_status(
        self,
        body: StatusBody,
    ) -> ResponseModel:
        return await self._controller.generation_status(
            body,
        )
