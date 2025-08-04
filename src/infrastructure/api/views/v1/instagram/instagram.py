# coding utf-8

from fastapi_pagination import Page

from ......interface.controllers.api.v1 import InstagramController

from ......domain.entities.instagram import ISession

from ......interface.schemas.external import (
    IInstagramUser,
    InstagramAuthResponse,
    InstagramUserResponse,
    InstagramUpdateUserResponse,
    InstagramFollower,
    InstagramPost,
)


class InstagramView:
    def __init__(
        self,
        controller: InstagramController,
    ) -> None:
        self._controller = controller

    async def auth_user_session(
        self,
        body: ISession,
    ) -> InstagramAuthResponse:
        return await self._controller.auth_user_session(
            body,
        )

    async def update_user_data(
        self,
        body: IInstagramUser,
        uuid: str,
    ) -> InstagramUpdateUserResponse:
        return await self._controller.update_user_data(
            body,
            uuid,
        )

    async def fetch_statistics(
        self,
        body: IInstagramUser,
        uuid: str,
    ) -> InstagramUserResponse:
        return await self._controller.fetch_statistics(
            body,
            uuid,
        )

    async def fetch_publication(
        self,
        body: IInstagramUser,
        uuid: str,
        id: int,
    ) -> InstagramPost:
        return await self._controller.fetch_publication(
            body,
            uuid,
            id,
        )

    async def fetch_subscribers(
        self,
        body: IInstagramUser,
        uuid: str,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_subscribers(
            body,
            uuid,
        )

    async def fetch_subscribtions(
        self,
        body: IInstagramUser,
        uuid: str,
        relation_type: str,
    ) -> Page[InstagramFollower]:
        return await self._controller.fetch_subscribtions(
            body,
            uuid,
            relation_type,
        )

    # async def fetch_non_reciprocal_subsribtions(
    #     self,
    #     body: IInstagramUser,
    # ) -> Page[InstagramFollower]:
    #     return await self._controller.fetch_non_reciprocal_subsribtions(
    #         body,
    #     )

    # async def fetch_publications(
    #     self,
    #     body: IInstagramUser,
    # ) -> Page[InstagramPost]:
    #     return await self._controller.fetch_publications(
    #         body,
    #     )
