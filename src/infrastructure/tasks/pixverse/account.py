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
        data: AccountBalance,
    ) -> AccountBalance:
        return await self._repository.update_record(
            account.id,
            data=data,
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
    ) -> Any:
        balance: TokensResponse = await self.fetch_account_balance(
            account,
        )
        if balance.credits != account.balance:
            return await self.update_account_record(
                account,
                data=AccountBalance(
                    balance=balance.credits,
                    is_active=False
                    if account.balance <= 100 and account.is_active is True
                    else True,
                ),
            )

    async def update_accounts(
        self,
    ) -> Any:
        accounts: list[Any] | None = await self._repository.fetch_all()
        for acc in accounts:
            await self.update_account_balance(
                acc,
            )
