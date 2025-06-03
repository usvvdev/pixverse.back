# coding utf-8

from .....interface.controllers.api.v1 import PixverseTemplateController

from .....interface.schemas.api import (
    Template,
    ITemplate,
    ChangeTemplate,
)


class PixverseTemplateView:
    def __init__(
        self,
        controller: PixverseTemplateController,
    ) -> None:
        self._controller = controller

    async def fetch_templates(
        self,
    ) -> list[Template]:
        return await self._controller.fetch_templates()

    async def fetch_template_by_template_id(
        self,
        template_id: int,
    ) -> Template:
        return await self._controller.fetch_template_by_template_id(
            template_id,
        )

    async def fetch_template_by_id(
        self,
        id: int,
    ) -> Template:
        return await self._controller.fetch_template_by_id(
            id,
        )

    async def add_template(
        self,
        data: ITemplate,
        preview_small: str,
        preview_large: str,
    ) -> ChangeTemplate:
        return await self._controller.add_template(
            data,
            preview_small,
            preview_large,
        )

    async def update_template(
        self,
        id: int,
        data: ITemplate,
        preview_small: str,
        preview_large: str,
    ) -> ChangeTemplate:
        return await self._controller.update_template(
            id,
            data,
            preview_small,
            preview_large,
        )

    async def delete_template(
        self,
        id: int,
    ) -> bool:
        return await self._controller.delete_template(
            id,
        )
