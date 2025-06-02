# coding utf-8

from ..models import PixverseAccounts

from .....domain.repositories import (
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
