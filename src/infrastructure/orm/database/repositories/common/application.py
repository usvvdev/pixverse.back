# coding utf-8

from ...models import Applications

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class ApplicationRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            Applications,
        )

    async def fetch_application(
        self,
        field_name: str,
        value: str | int,
    ) -> Applications | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )
