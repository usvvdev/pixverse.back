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
    "/statistics",
)
async def fetch_statistics(
    body: IInstagramUser,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> InstagramUserResponse:
    return await view.fetch_statistics(
        body,
    )


@instagram_router.post(
    "/subscribers",
)
async def fetch_subsribers(
    body: IInstagramUser,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[InstagramFollower]:
    return await view.fetch_subsribers(
        body,
    )


@instagram_router.post(
    "/subscribtions",
)
async def fetch_subsribtions(
    body: IInstagramUser,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[InstagramFollower]:
    return await view.fetch_subsribtions(
        body,
    )


@instagram_router.post(
    "/non-reciprocal-subscribers",
)
async def fetch_non_reciprocal_subsribtions(
    body: IInstagramUser,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[InstagramFollower]:
    return await view.fetch_non_reciprocal_subsribtions(
        body,
    )


@instagram_router.post(
    "/publications",
)
async def fetch_publications(
    body: IInstagramUser,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[InstagramFollower]:
    return await view.fetch_publications(
        body,
    )
