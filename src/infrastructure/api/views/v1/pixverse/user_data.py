# coding utf-8

from ......interface.controllers.api.v1 import UserDataController

from ......domain.entities.core import IUserData

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
        app_name: str | None,
    ) -> list[UserStatistics]:
        return await self._controller.fetch_user_data(
            user_id,
            app_id,
            app_name,
        )

    async def fetch_user_filters(
        self,
        app_name: str | None,
    ) -> UserFilters:
        return await self._controller.fetch_user_filters(
            app_name,
        )

    async def fetch_user_tokens(
        self,
        user_id: str,
        app_id: str,
    ) -> IUserData:
        return await self._controller.fetch_user_tokens(
            user_id,
            app_id,
        )
