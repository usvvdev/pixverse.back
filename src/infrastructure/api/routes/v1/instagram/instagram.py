# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from fastapi_pagination import Page

from ....views.v1 import InstagramView

from ......domain.tools import auto_docs

from ......domain.typing.enums import InstagramRelationType

from ......interface.schemas.external import (
    IInstagramUser,
    InstagramAuthUser,
    InstagramAuthResponse,
    InstagramSessionResponse,
    InstagramUserResponse,
    InstagramFollower,
)

from .....factroies.api.v1 import InstagramViewFactory


instagram_router = APIRouter(tags=["Instagram"])


@instagram_router.post(
    "/auth",
)
async def user_auth(
    body: InstagramAuthUser,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> InstagramAuthResponse | InstagramSessionResponse:
    return await view.user_auth(
        body,
    )


@instagram_router.post(
    "/users/statistics",
)
async def fetch_user_statistics(
    body: IInstagramUser,
    search_user: str | None = None,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> InstagramUserResponse:
    return await view.fetch_user_statistics(
        body,
        search_user,
    )


@instagram_router.post(
    "/users",
)
async def fetch_users(
    body: IInstagramUser,
    type: InstagramRelationType = Query(InstagramRelationType.FOLLOWERS),
    search_user: str | None = Query(None),
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[InstagramFollower]:
    return await view.fetch_users(
        body,
        type,
        search_user,
    )
