# coding utf-8

from typing import Any

from .core import PixverseCelery

from ....domain.repositories import IDatabase

from ...orm.database.models import PixverseAccounts

from ...orm.database.repositories import PixverseAccountRepository

from ....interface.schemas.external import (
    AuthRes,
    TokensResponse,
)

from ....interface.schemas.api import AccountBalance


class PixverseAccountCelery(PixverseCelery):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self._repository = PixverseAccountRepository(
            IDatabase(self._conf),
        )

    async def update_account_record(
        self,
        account: PixverseAccounts,
        balance: int,
        is_active: bool = True,
    ) -> AccountBalance:
        return await self._repository.update_record(
            account.id,
            data=AccountBalance(
                balance=balance,
                is_active=is_active,
            ),
        )

    async def fetch_account_token(
        self,
        account: PixverseAccounts,
    ) -> AuthRes:
        return await self.client.auth_user(
            account,
        )

    async def fetch_account_balance(
        self,
        account: PixverseAccounts,
    ) -> TokensResponse:
        token: AuthRes = await self.fetch_account_token(
            account,
        )
        return await self.client.credits_amount(
            token.access_token,
        )

    async def update_account_balance(
        self,
        account: PixverseAccounts,
        is_active: bool = False,
    ) -> Any:
        balance: TokensResponse = await self.fetch_account_balance(
            account,
        )
        if balance.credits != account.balance:
            return await self.update_account_record(
                account,
                balance.credits,
            )
        elif account.balance <= 100 and account.is_active is True:
            return await self.update_account_record(
                account,
                balance.credits,
                is_active,
            )

    async def update_accounts(
        self,
    ) -> Any:
        accounts: list[Any] | None = await self._repository.fetch_all()
        for acc in accounts:
            await self.update_account_balance(
                acc,
            )
