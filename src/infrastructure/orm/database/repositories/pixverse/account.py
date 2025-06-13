# coding utf-8

from ...models import PixverseAccounts

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class PixverseAccountRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            PixverseAccounts,
        )

    async def fetch_account(
        self,
        field_name: str,
        value: str | int,
    ) -> PixverseAccounts | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )

    async def fetch_next_account(
        self,
    ):
        account = await self.fetch_one_with_filters(
            where="is_active",
            value=True,
            order_by="usage_count",
        )
        await self.update_record(
            id=account.id, data={"usage_count": int(1 + account.usage_count)}
        )
        return account
