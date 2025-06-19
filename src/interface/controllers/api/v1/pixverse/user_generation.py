# coding utf-8

from ......infrastructure.orm.database.repositories import (
    UserDataRepository,
)

from .....schemas.api import (
    UserData,
)


class UserDataController:
    def __init__(
        self,
        repository: UserDataRepository,
    ) -> None:
        self._repository = repository

    async def fetch_user_data(
        self,
    ) -> list[UserData]:
        return await self._repository.fetch_all()
