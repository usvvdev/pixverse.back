# coding utf-8

from typing import Any

from .....interface.schemas.api import (
    TextBody,
    ImageBody,
    StatusBody,
)

from .....interface.controllers.api.v1 import PixVerseController


class PixVerseView:
    def __init__(
        self,
        controller: PixVerseController,
    ) -> None:
        self._controller = controller

    async def text_to_video(
        self,
        body: TextBody,
    ) -> dict[str, Any]:
        return await self._controller.text_to_video(
            body,
        )

    async def image_to_video(
        self,
        body: ImageBody,
    ) -> dict[str, Any]:
        return await self._controller.image_to_video(
            body,
        )

    async def generation_status(
        self,
        body: StatusBody,
    ) -> dict[str, Any]:
        return await self._controller.generation_status(
            body,
        )
