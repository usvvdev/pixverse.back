# coding utf-8

from ......infrastructure.orm.database.repositories import PixverseAccountRepository

from .....schemas.api import (
    Account,
    IAccount,
    AddAccount,
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
        token_data: dict[str, str | int],
    ) -> list[Account]:
        return await self._repository.fetch_with_filters(
            many=True,
            auth_user_id=token_data.get("aid"),
        )

    async def fetch_account(
        self,
        id: int,
        token_data: dict[str, str | int],
    ) -> Account | None:
        return await self._repository.fetch_one_with_filters(
            id=id,
            auth_user_id=token_data.get("aid"),
        )

    async def add_account(
        self,
        data: IAccount,
        token_data: dict[str, str | int],
    ) -> ChangeAccount:
        account_data = AddAccount(
            **data.dict,
            user_id=token_data.get("aid"),
        )
        return await self._repository.add_record(
            account_data,
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
