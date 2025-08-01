# coding utf-8

from fastapi_pagination import Page

from .....schemas.external import (
    IInstagramUser,
    InstagramAuthUser,
    InstagramAuthResponse,
    InstagramSessionResponse,
    InstagramUserResponse,
    InstagramFollower,
    InstagramPost,
)

from ......domain.entities.instagram import ISession

from ......domain.typing.enums import InstagramRelationType

from ......infrastructure.external.instagram import InstagramClient


class InstagramController:
    def __init__(
        self,
        client: InstagramClient,
    ) -> None:
        self._client = client

    async def auth_user_session(
        self,
        body: ISession,
    ) -> InstagramAuthResponse:
        return await self._client.auth_user_session(
            body,
        )

    async def fetch_statistics(
        self,
        body: IInstagramUser,
        uuid: str,
    ) -> InstagramUserResponse:
        return await self._client.fetch_statistics(
            body,
            uuid,
        )

    async def fetch_publication(
        self,
        body: IInstagramUser,
        uuid: str,
        id: int,
    ) -> InstagramPost:
        return await self._client.fetch_publication(
            body,
            uuid,
            id,
        )

    async def fetch_subscribers(
        self,
        body: IInstagramUser,
        uuid: str,
    ) -> Page[InstagramFollower]:
        return await self._client.fetch_subscribers(
            body,
            uuid,
        )

    async def fetch_subscribtions(
        self,
        body: IInstagramUser,
        uuid: str,
    ) -> Page[InstagramFollower]:
        return await self._client.fetch_subscribtions(
            body,
            uuid,
        )

    # async def fetch_subsribers(
    #     self,
    #     body: IInstagramUser,
    # ) -> Page[InstagramFollower]:
    #     return await self._client.fetch_subsribers(
    #         body,
    #     )

    # async def fetch_subsribtions(
    #     self,
    #     body: IInstagramUser,
    # ) -> Page[InstagramFollower]:
    #     return await self._client.fetch_subsribtions(
    #         body,
    #     )

    # async def fetch_non_reciprocal_subsribtions(
    #     self,
    #     body: IInstagramUser,
    # ) -> Page[InstagramFollower]:
    #     return await self._client.fetch_non_reciprocal_subsribtions(
    #         body,
    #     )

    # async def fetch_publications(
    #     self,
    #     body: IInstagramUser,
    # ) -> Page[InstagramPost]:
    #     return await self._client.fetch_publications(
    #         body,
    #     )
