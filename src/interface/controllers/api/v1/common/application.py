# coding utf-8

from ......infrastructure.orm.database.repositories import ApplicationRepository

from ......interface.schemas.api import (
    StoreApplication,
    ChangeStoreApplication,
    AddStoreApplication,
)


class ApplicationController:
    def __init__(
        self,
        repository: ApplicationRepository,
    ) -> None:
        self._repository = repository

    async def fetch_applications(
        self,
    ) -> list[StoreApplication]:
        return await self._repository.fetch_all(
            ["products"],
        )

    async def fetch_application(
        self,
        id: int,
    ) -> StoreApplication:
        return await self._repository.fetch_application(
            "id",
            id,
        )

    async def add_application(
        self,
        data: AddStoreApplication,
    ) -> AddStoreApplication:
        return await self._repository.add_record(
            data,
        )

    async def delete_application(
        self,
        id: int,
    ) -> bool:
        return await self._repository.delete_record(
            id,
        )

    async def update_application(
        self,
        id: int,
        data: ChangeStoreApplication,
    ) -> ChangeStoreApplication:
        return await self._repository.update_record(
            id,
            data,
        )
