# coding utf-8

from .....interface.controllers.api.v1 import ApplicationController

from .....interface.schemas.api import (
    Application,
    IApplication,
    ChangeApplication,
)


class ApplicationView:
    def __init__(
        self,
        controller: ApplicationController,
    ) -> None:
        self._controller = controller

    async def fetch_applications(
        self,
    ) -> list[Application]:
        return await self._controller.fetch_applications()

    async def fetch_application_by_app_id(
        self,
        app_id: str,
    ) -> Application:
        return await self._controller.fetch_application_by_app_id(
            app_id,
        )

    async def add_application(
        self,
        data: IApplication,
    ) -> IApplication:
        return await self._controller.add_application(
            data,
        )

    async def update_application(
        self,
        id: int,
        data: ChangeApplication,
    ) -> IApplication:
        return await self._controller.update_application(
            id,
            data,
        )

    async def delete_application(
        self,
        id: int,
    ) -> bool:
        return await self._controller.delete_application(
            id,
        )
