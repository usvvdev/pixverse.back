# coding utf-8

from .....infrastructure.orm.database.repositories import PixverseTemplateRepository

from ....schemas.api import Template


class PixverseTemplateController:
    def __init__(
        self,
        repository: PixverseTemplateRepository,
    ) -> None:
        self._repository = repository

    async def fetch_templates(
        self,
    ) -> list[Template]:
        return await self._repository.fetch_all()

    async def fetch_template_by_template_id(
        self,
        template_id: int,
    ) -> Template | None:
        return await self._repository.fetch_template(
            "template_id",
            template_id,
        )

    async def fetch_template_by_id(
        self,
        id: int,
    ) -> Template | None:
        return await self._repository.fetch_template(
            "id",
            id,
        )

    async def add_template(
        self,
        data: Template,
    ) -> Template:
        return await self._repository.add_record(
            data,
        )

    async def update_template(
        self,
        id: int,
        data: Template,
    ) -> Template:
        return await self._repository.update_record(
            id,
            data,
        )

    async def delete_template(
        self,
        id: int,
    ) -> Template:
        return await self._repository.delete_record(
            id,
        )
