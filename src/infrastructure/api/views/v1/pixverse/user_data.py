# coding utf-8

from ......interface.controllers.api.v1 import UserDataController

from ......interface.schemas.api import (
    UserData,
)


class UserDataView:
    def __init__(
        self,
        controller: UserDataController,
    ) -> None:
        self._controller = controller

    async def fetch_user_data(
        self,
    ) -> list[UserData]:
        return await self._controller.fetch_user_data()
