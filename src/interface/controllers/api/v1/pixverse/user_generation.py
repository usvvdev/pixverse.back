# coding utf-8

from ......infrastructure.orm.database.repositories import (
    UserDataRepository,
)

from .....schemas.external import (
    UserStatistics,
    UserFilters,
)


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

    async def fetch_user_filters(
        self,
    ) -> UserFilters:
        data: list[UserStatistics] = await self._repository.fetch_all()
        return UserFilters(
            user_ids=list({item.user_id for item in data}),
            app_ids=list({item.app_id for item in data}),
        )
