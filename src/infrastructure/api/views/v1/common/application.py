# coding utf-8

from ......interface.controllers.api.v1 import ApplicationController

from ......interface.schemas.api import (
    StoreApplication,
    ChangeStoreApplication,
    AddStoreApplication,
)


class ApplicationView:
    def __init__(
        self,
        controller: ApplicationController,
    ) -> None:
        self._controller = controller

    async def fetch_applications(
        self,
    ) -> list[StoreApplication]:
        return await self._controller.fetch_applications()

    async def fetch_application(
        self,
        id: int,
    ) -> StoreApplication:
        return await self._controller.fetch_application(
            id,
        )

    async def add_application(
        self,
        data: AddStoreApplication,
    ) -> AddStoreApplication:
        return await self._controller.add_application(
            data,
        )

    async def update_application(
        self,
        id: int,
        data: ChangeStoreApplication,
    ) -> ChangeStoreApplication:
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
