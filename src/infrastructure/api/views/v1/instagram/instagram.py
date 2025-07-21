# coding utf-8

from fastapi_pagination import Page

from ......interface.controllers.api.v1 import InstagramController

from ......domain.typing.enums import InstagramRelationType

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

    async def fetch_statistics(
        self,
        body: IInstagramUser,
    ) -> InstagramUserResponse:
        return await self._controller.fetch_statistics(
            body,
        )

    async def fetch_subsribers(
        self,
        body: IInstagramUser,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_subsribers(
            body,
        )

    async def fetch_subsribtions(
        self,
        body: IInstagramUser,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_subsribtions(
            body,
        )

    async def fetch_non_reciprocal_subsribtions(
        self,
        body: IInstagramUser,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_non_reciprocal_subsribtions(
            body,
        )

    async def fetch_publications(
        self,
        body: IInstagramUser,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_publications(
            body,
        )
