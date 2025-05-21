# coding utf-8

from typing import Any

from ....schemas.api import (
    TextBody,
    ImageBody,
    StatusBody,
)

from .....infrastructure.external.pixverse import PixVerseClient


class PixVerseController:
    def __init__(
        self,
        client: PixVerseClient,
    ) -> None:
        self._client = client

    async def text_to_video(
        self,
        body: TextBody,
    ) -> dict[str, Any]:
        return await self._client.text_to_video(
            body,
        )

    async def image_to_video(
        self,
        body: ImageBody,
    ) -> dict[str, Any]:
        return await self._client.image_to_video(
            body,
        )

    async def generation_status(
        self,
        body: StatusBody,
    ) -> dict[str, Any]:
        return await self._client.generation_status(
            body,
        )
