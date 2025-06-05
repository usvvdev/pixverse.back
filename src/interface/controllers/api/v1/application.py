# coding utf-8

from .....domain.conf import app_conf

from .....domain.entities.core import IConfEnv

from .....domain.repositories import IDatabase

from .....infrastructure.orm.database.repositories import (
    ApplicationRepository,
    PixverseTemplateRepository,
)

from ....schemas.api import (
    Template,
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
        return await self._repository.fetch_all()

    async def fetch_application_by_id(
        self,
        id: int,
    ) -> Application | None:
        return await self._repository.fetch_application(
            "id",
            id,
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
        return await self._repository.update_record(
            id,
            IApplication(
                **data.dict,
                templates=Template.create(
                    await template_database.fetch_templates_by_id(
                        data.ids,
                    ),
                ),
            ),
        )

    async def delete_application(
        self,
        id: int,
    ) -> bool:
        return await self._repository.delete_record(
            id,
        )
