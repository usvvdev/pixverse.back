# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
)

from ......domain.entities.qwen import IT2IBody

from ....views.v1 import QwenView

from ......interface.schemas.external import QwenPhotoAPIResponse

from .....factroies.api.v1 import QwenViewFactory


qwen_router = APIRouter(tags=["Qwen"])


@qwen_router.post(
    "/text2photo",
    response_model=QwenPhotoAPIResponse,
    response_model_exclude_none=True,
)
async def text_to_photo(
    body: IT2IBody,
    app_id: str,
    user_id: str,
    view: QwenView = Depends(QwenViewFactory.create),
) -> QwenPhotoAPIResponse:
    return await view.text_to_photo(
        body,
    )


@qwen_router.post(
    "/test",
    # response_model=QwenPhotoAPIResponse,
    # response_model_exclude_none=True,
)
async def photo_to_photo(
    # body: IT2IBody,
    token: str,
    image: UploadFile,
    view: QwenView = Depends(QwenViewFactory.create),
):
    return await view.fetch_upload_token(
        token,
        image,
    )
