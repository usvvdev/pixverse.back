# coding utf-8

from .....interface.controllers.api.v1 import PixverseTemplateController

from .....interface.schemas.api import Template


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
        data: Template,
    ) -> Template:
        return await self._controller.add_template(
            data,
        )

    async def update_template(
        self,
        id: int,
        data: Template,
    ) -> Template:
        return await self._controller.update_template(
            id,
            data,
        )

    async def delete_template(
        self,
        id: int,
    ) -> Template:
        return await self._controller.delete_template(
            id,
        )
