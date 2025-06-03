# coding utf-8

from .....interface.controllers.api.v1 import PixverseStyleController

from .....interface.schemas.api import Style


class PixverseStyleView:
    def __init__(
        self,
        controller: PixverseStyleController,
    ) -> None:
        self._controller = controller

    async def fetch_styles(
        self,
    ) -> list[Style]:
        return await self._controller.fetch_styles()

    async def fetch_style_by_template_id(
        self,
        template_id: int,
    ) -> Style:
        return await self._controller.fetch_style_by_template_id(
            template_id,
        )

    async def fetch_style_by_id(
        self,
        id: int,
    ) -> Style:
        return await self._controller.fetch_style_by_id(
            id,
        )

    async def add_style(
        self,
        data: Style,
    ) -> Style:
        return await self._controller.add_style(
            data,
        )

    async def update_style(
        self,
        id: int,
        data: Style,
    ) -> Style:
        return await self._controller.update_style(
            id,
            data,
        )

    async def delete_style(
        self,
        id: int,
    ) -> Style:
        return await self._controller.delete_style(
            id,
        )
