# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from fastapi_pagination import Page

from ....views.v1 import InstagramView

from ......domain.tools import auto_docs

from ......domain.entities.instagram import ISession

from ......domain.typing.enums import InstagramRelationType

from ......interface.schemas.external import (
    IInstagramUser,
    InstagramAuthUser,
    InstagramAuthResponse,
    InstagramSessionResponse,
    InstagramUserResponse,
    InstagramFollower,
    InstagramPost,
    IInstagramPost,
)

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
    "/users/{uuid}/statistics",
)
async def fetch_statistics(
    body: IInstagramUser,
    uuid: str,
    view: InstagramView = Depends(InstagramViewFactory.create),
):
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
) -> IInstagramPost:
    return await view.fetch_subscribers(
        body,
        uuid,
    )


# @instagram_router.post(
#     "/subscribers",
# )
# async def fetch_subsribers(
#     body: IInstagramUser,
#     view: InstagramView = Depends(InstagramViewFactory.create),
# ) -> Page[InstagramFollower]:
#     return await view.fetch_subsribers(
#         body,
#     )


# @instagram_router.post(
#     "/subscribtions",
# )
# async def fetch_subsribtions(
#     body: IInstagramUser,
#     view: InstagramView = Depends(InstagramViewFactory.create),
# ) -> Page[InstagramFollower]:
#     return await view.fetch_subsribtions(
#         body,
#     )


# @instagram_router.post(
#     "/non-reciprocal-subscribers",
# )
# async def fetch_non_reciprocal_subsribtions(
#     body: IInstagramUser,
#     view: InstagramView = Depends(InstagramViewFactory.create),
# ) -> Page[InstagramFollower]:
#     return await view.fetch_non_reciprocal_subsribtions(
#         body,
#     )


# @instagram_router.post(
#     "/publications",
# )
# async def fetch_publications(
#     body: IInstagramUser,
#     view: InstagramView = Depends(InstagramViewFactory.create),
# ) -> Page[InstagramPost]:
#     return await view.fetch_publications(
#         body,
#     )
