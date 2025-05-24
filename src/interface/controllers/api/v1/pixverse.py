# coding utf-8

from ....schemas.api import (
    StatusBody,
    UserCredentials,
)

from .....domain.entities import IBody

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
        body: IBody,
    ) -> ResponseModel:
        return await self._client.text_to_video(
            token,
            body,
        )

    async def image_to_video(
        self,
        body: IBody,
        token: str,
        file: str,
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
