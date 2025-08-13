# coding utf-8

from ......domain.entities.qwen import (
    IT2IBody,
)

from ......interface.schemas.external import QwenPhotoAPIResponse

from ......interface.controllers.api.v1 import QwenController


class QwenView:
    def __init__(
        self,
        controller: QwenController,
    ) -> None:
        self._controller = controller

    async def text_to_photo(
        self,
        body: IT2IBody,
    ) -> QwenPhotoAPIResponse:
        return await self._controller.text_to_photo(
            body,
        )
