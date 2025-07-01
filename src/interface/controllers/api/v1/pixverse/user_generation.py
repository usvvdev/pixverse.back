# coding utf-8

from ......infrastructure.orm.database.repositories import (
    UserDataRepository,
)

from .....schemas.external import UserStatistics


class UserDataController:
    def __init__(
        self,
        repository: UserDataRepository,
    ) -> None:
        self._repository = repository

    async def fetch_user_data(
        self,
    ) -> list[UserStatistics]:
        return await self._repository.fetch_all()
