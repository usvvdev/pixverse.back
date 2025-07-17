# coding utf-8

from fastapi_pagination import Page

from .....schemas.external import (
    IInstagramUser,
    InstagramAuthUser,
    InstagramAuthResponse,
    InstagramSessionResponse,
    InstagramUserResponse,
    InstagramFollower,
)

from ......infrastructure.external.instagram import InstagramClient


class InstagramController:
    def __init__(
        self,
        client: InstagramClient,
    ) -> None:
        self._client = client

    async def user_auth(
        self,
        body: InstagramAuthUser,
    ) -> InstagramAuthResponse | InstagramSessionResponse:
        return await self._client.user_auth(
            body,
        )

    async def fetch_user_statistics(
        self,
        body: IInstagramUser,
        search_user: str | None,
    ) -> InstagramUserResponse:
        return await self._client.fetch_user_statistics(
            body,
            search_user,
        )

    async def fetch_subscribers(
        self,
        body: IInstagramUser,
        search_user: str | None = None,
    ) -> Page[InstagramFollower]:
        return await self._client.fetch_subscribers(
            body,
            search_user,
        )

    async def fetch_subsribtions(
        self,
        body: IInstagramUser,
        search_user: str | None = None,
    ) -> Page[InstagramFollower]:
        return await self._client.fetch_subsribtions(
            body,
            search_user,
        )
