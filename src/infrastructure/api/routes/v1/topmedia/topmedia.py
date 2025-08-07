# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ......domain.entities.topmedia import (
    IT2SBody,
    ITSGBody,
)

from ....views.v1 import TopmediaView

from ......interface.schemas.external import TopmediaAPIResponse

from .....factroies.api.v1 import TopmediaViewFactory


topmedia_router = APIRouter(tags=["TopMedia"])


@topmedia_router.post(
    "/text2speech",
    response_model=TopmediaAPIResponse,
    response_model_exclude_none=True,
)
async def text_to_speech(
    body: IT2SBody,
    app_bundle_id: str,
    user_id: str,
    view: TopmediaView = Depends(TopmediaViewFactory.create),
) -> TopmediaAPIResponse:
    return await view.text_to_speech(
        body,
    )


@topmedia_router.post(
    "/text2song",
    response_model=TopmediaAPIResponse,
    response_model_exclude_none=True,
)
async def text_to_song(
    body: ITSGBody,
    app_bundle_id: str,
    user_id: str,
    view: TopmediaView = Depends(TopmediaViewFactory.create),
) -> TopmediaAPIResponse:
    return await view.text_to_song(
        body,
    )
