# coding utf-8

from ......infrastructure.orm.database.repositories import PixverseAccountRepository

from .....schemas.api import (
    Account,
    IAccount,
    ChangeAccount,
)


class PixverseAccountController:
    def __init__(
        self,
        repository: PixverseAccountRepository,
    ) -> None:
        self._repository = repository

    async def fetch_accounts(
        self,
    ) -> list[Account]:
        return await self._repository.fetch_all()

    async def fetch_account(
        self,
        id: int,
    ) -> Account | None:
        return await self._repository.fetch_account(
            "id",
            id,
        )

    async def add_account(
        self,
        data: IAccount,
    ) -> ChangeAccount:
        return await self._repository.add_record(
            data,
        )

    async def update_account(
        self,
        id: int,
        data: ChangeAccount,
    ) -> ChangeAccount:
        return await self._repository.update_record(
            id,
            data,
        )

    async def delete_account(
        self,
        id: int,
    ) -> bool:
        return await self._repository.delete_record(
            id,
        )
