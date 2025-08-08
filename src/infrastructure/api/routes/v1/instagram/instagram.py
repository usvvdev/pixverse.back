# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
)

from typing import Literal

from fastapi_pagination import Page

from ....views.v1 import InstagramView

from ......domain.tools import auto_docs

from ......domain.entities.instagram import ISession

from ......interface.schemas.external import (
    IInstagramUser,
    InstagramUser,
    InstagramAuthResponse,
    InstagramUserResponse,
    InstagramUpdateUserResponse,
    InstagramTrackingUserResponse,
    InstagramFollower,
    IInstagramPost,
    T2PBody,
    ChatGPTInstagram,
)

from ......interface.schemas.api import SearchUser

from .....factroies.api.v1 import InstagramViewFactory


instagram_router = APIRouter(tags=["Instagram"])


@instagram_router.post(
    "/users/session",
)
async def auth_user_session(
    body: ISession,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> InstagramAuthResponse:
    return await view.auth_user_session(
        body,
    )


@instagram_router.post(
    "/users/{uuid}/search/{username}",
)
async def find_user(
    body: IInstagramUser,
    uuid: str,
    username: str,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> SearchUser:
    return await view.find_user(
        uuid,
        username,
    )


@instagram_router.post(
    "/users/{uuid}/tracking/{user_id}",
)
async def add_user_tracking(
    body: IInstagramUser,
    uuid: str,
    user_id: int,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> InstagramTrackingUserResponse:
    return await view.add_user_tracking(
        uuid,
        user_id,
    )


@instagram_router.post(
    "/users/{uuid}/tracking",
)
async def fetch_user_tracking(
    body: IInstagramUser,
    uuid: str,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[InstagramUser]:
    return await view.fetch_user_tracking(
        uuid,
    )


@instagram_router.post(
    "/users/{uuid}/update",
)
async def update_user_data(
    body: IInstagramUser,
    uuid: str,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> InstagramUpdateUserResponse:
    return await view.update_user_data(
        body,
        uuid,
    )


@instagram_router.post(
    "/users/{uuid}/statistics",
)
async def fetch_statistics(
    body: IInstagramUser,
    uuid: str,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> InstagramUserResponse:
    return await view.fetch_statistics(
        body,
        uuid,
    )


@instagram_router.post(
    "/users/{uuid}/publications/{id}",
)
async def fetch_publication(
    body: IInstagramUser,
    uuid: str,
    id: int,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> IInstagramPost:
    return await view.fetch_publication(
        body,
        uuid,
        id,
    )


@instagram_router.post(
    "/users/{uuid}/subscribers",
)
async def fetch_subscribers(
    body: IInstagramUser,
    uuid: str,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[InstagramFollower]:
    return await view.fetch_subscribers(
        body,
        uuid,
    )


@instagram_router.post(
    "/users/{uuid}/subscribtions",
)
async def fetch_subscribtions(
    body: IInstagramUser,
    uuid: str,
    relation_type: Literal["mutual", "not_followed_by"] = "mutual",
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[InstagramFollower]:
    return await view.fetch_subscribtions(
        body,
        uuid,
        relation_type,
    )


@instagram_router.post(
    "/users/{uuid}/text2post",
)
async def text_to_post(
    uuid: str,
    body: T2PBody,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> ChatGPTInstagram:
    return await view.image_to_post(
        uuid,
        body,
    )
