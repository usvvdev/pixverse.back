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

from ......domain.typing.enums import InstagramRelationType

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

    async def fetch_statistics(
        self,
        body: IInstagramUser,
    ) -> InstagramUserResponse:
        return await self._client.fetch_statistics(
            body,
        )

    async def fetch_subsribers(
        self,
        body: IInstagramUser,
    ) -> Page[InstagramFollower]:
        return await self._client.fetch_subsribers(
            body,
        )

    async def fetch_subsribtions(
        self,
        body: IInstagramUser,
    ) -> Page[InstagramFollower]:
        return await self._client.fetch_subsribtions(
            body,
        )

    async def fetch_non_reciprocal_subsribtions(
        self,
        body: IInstagramUser,
    ) -> Page[InstagramFollower]:
        return await self._client.fetch_non_reciprocal_subsribtions(
            body,
        )

    async def fetch_publications(
        self,
        body: IInstagramUser,
    ) -> Page[InstagramFollower]:
        return await self._client.fetch_publications(
            body,
        )
