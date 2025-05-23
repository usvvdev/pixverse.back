# coding utf-8

from fastapi import UploadFile

from ....schemas.api import (
    BaseBody,
    TextBody,
    StatusBody,
    UserCredentials,
)

from .....infrastructure.external.pixverse import PixVerseClient

from .....interface.schemas.api import ResponseModel


class PixVerseController:
    def __init__(
        self,
        client: PixVerseClient,
    ) -> None:
        self._client = client

    async def auth_user(
        self,
        body: UserCredentials,
    ) -> ResponseModel:
        return await self._client.auth_user(
            body,
        )

    async def text_to_video(
        self,
        token: str,
        body: TextBody,
    ) -> ResponseModel:
        return await self._client.text_to_video(
            token,
            body,
        )

    async def image_to_video(
        self,
        body: BaseBody,
        token: str,
        file: UploadFile,
    ):
        return await self._client.image_to_video(
            body,
            token,
            file,
        )

    async def generation_status(
        self,
        body: StatusBody,
    ) -> ResponseModel:
        return await self._client.generation_status(
            body,
        )
