# coding utf-8

from fastapi_pagination import Page

from ......interface.controllers.api.v1 import InstagramController

from ......interface.schemas.external import (
    IInstagramUser,
    InstagramAuthUser,
    InstagramAuthResponse,
    InstagramSessionResponse,
    InstagramUserResponse,
    InstagramFollower,
)


class InstagramView:
    def __init__(
        self,
        controller: InstagramController,
    ) -> None:
        self._controller = controller

    async def user_auth(
        self,
        body: InstagramAuthUser,
    ) -> InstagramAuthResponse | InstagramSessionResponse:
        return await self._controller.user_auth(
            body,
        )

    async def fetch_user_statistics(
        self,
        body: IInstagramUser,
        search_user: str | None,
    ) -> InstagramUserResponse:
        return await self._controller.fetch_user_statistics(
            body,
            search_user,
        )

    async def fetch_subscribers(
        self,
        body: IInstagramUser,
        search_user: str | None = None,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_subscribers(
            body,
            search_user,
        )

    async def fetch_subsribtions(
        self,
        body: IInstagramUser,
        search_user: str | None = None,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_subsribtions(
            body,
            search_user,
        )
