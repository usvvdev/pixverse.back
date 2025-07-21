# coding utf-8

from ......interface.controllers.api.v1 import UserDataController

from ......interface.schemas.external import (
    UserStatistics,
    UserFilters,
)


class UserDataView:
    def __init__(
        self,
        controller: UserDataController,
    ) -> None:
        self._controller = controller

    async def fetch_user_data(
        self,
        user_id: str | None,
        app_id: str | None,
    ) -> list[UserStatistics]:
        return await self._controller.fetch_user_data(
            user_id,
            app_id,
        )

    async def fetch_user_filters(
        self,
    ) -> UserFilters:
        return await self._controller.fetch_user_filters()
