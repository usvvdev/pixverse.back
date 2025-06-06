# coding utf-8

from .....domain.conf import app_conf

from .....domain.entities.core import IConfEnv

from .....domain.repositories import IDatabase

from .....infrastructure.orm.database.repositories import (
    ApplicationRepository,
    PixverseTemplateRepository,
)

from .....infrastructure.orm.database.models import (
    ApplicationTemplates,
    ApplicationStyles,
)

from ....schemas.api import (
    Template,
    Style,
    Application,
    IApplication,
    ChangeApplication,
)


conf: IConfEnv = app_conf()


template_database = PixverseTemplateRepository(
    IDatabase(conf),
)


class ApplicationController:
    def __init__(
        self,
        repository: ApplicationRepository,
    ) -> None:
        self._repository = repository

    async def fetch_applications(
        self,
    ) -> list[Application]:
        return await self._repository.fetch_all(
            ["templates", "styles"],
        )

    async def fetch_application_by_app_id(
        self,
        app_id: str,
    ) -> Application | None:
        return await self._repository.fetch_application(
            "app_id",
            app_id,
            ["templates", "styles"],
        )

    async def add_application(
        self,
        data: IApplication,
    ) -> IApplication:
        return await self._repository.add_record(
            data,
        )

    async def update_application(
        self,
        id: int,
        data: ChangeApplication,
    ) -> IApplication:
        await self._repository.update_application(
            application_id=id,
            relation_table=ApplicationTemplates,
            relation_ids=data.template_ids,
            relation_column_name="template_id",
        )

        await self._repository.update_application(
            application_id=id,
            relation_table=ApplicationStyles,
            relation_ids=data.style_ids,
            relation_column_name="style_id",
        )

        return data

    async def delete_application(
        self,
        id: int,
    ) -> bool:
        return await self._repository.delete_record(
            id,
        )
