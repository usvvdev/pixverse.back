# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ....views.v1 import InstagramView

from ......domain.tools import auto_docs

from ......interface.schemas.external import (
    IInstagramUser,
    InstagramAuthUser,
    InstagramAuthResponse,
    InstagramSessionResponse,
    InstagramUserResponse,
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
