# coding utf-8

from .....infrastructure.orm.database.models import PixverseAccounts

from .....infrastructure.orm.database.repositories import PixverseAccountRepository

from ....schemas.api import Account


class PixverseAccountController:
    def __init__(
        self,
        repository: PixverseAccountRepository,
    ) -> None:
        self._repository = repository

    async def fetch_accounts(
        self,
    ) -> list[PixverseAccounts]:
        return await self._repository.fetch_all()

    async def add_account(
        self,
        data: Account,
    ) -> Account:
        return await self._repository.add_record(
            data,
        )

    async def fetch_account(
        self,
        id: int,
    ) -> PixverseAccounts | None:
        return await self._repository.fetch_account(
            "id",
            id,
        )
