# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
)

from ...views.v1 import PixVerseView

from .....interface.schemas.api import (
    TextBody,
    BaseBody,
    StatusBody,
)

from ....factroies.api.v1 import PixVerseViewFactory

from .....domain.tools import auto_docs

from .....interface.schemas.api import Resp


pixverse_router = APIRouter()


@pixverse_router.post(
    "/t2v",
)
@auto_docs(
    "api/v1/t2v",
    "POST",
    description="Роутер для создания видео по заданому тексту и параметрам.",
    params={
        "duration": {
            "type": "integer",
            "description": "Длительность видео фрагмента в секундах..",
        },
        "model": {
            "type": "string",
            "description": "Версия ИИ модели для обработки (например, 'v3.5', 'v4').",
        },
        "quality": {
            "type": "string",
            "description": "Качество видео при обработке.",
        },
        "aspect_ratio": {
            "type": "string",
            "description": "Соотношение сторон видео (например, '16:9', '1:1', '9:16').",
        },
    },
)
async def text_to_video(
    body: TextBody = Depends(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
    return await view.text_to_video(
        body,
    )


@pixverse_router.post(
    "/i2v",
)
@auto_docs(
    "api/v1/i2v",
    "POST",
    description="Роутер для создания видео по загруженой фотографии и параметрам.",
    params={
        "duration": {
            "type": "integer",
            "description": "Длительность видео фрагмента в секундах..",
        },
        "model": {
            "type": "string",
            "description": "Версия ИИ модели для обработки (например, 'v3.5', 'v4').",
        },
        "quality": {
            "type": "string",
            "description": "Качество видео при обработке.",
        },
    },
)
async def image_to_video(
    body: BaseBody = Depends(),
    file: UploadFile = File(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
    return await view.image_to_video(
        body,
        file,
    )


@pixverse_router.post(
    "/status",
)
@auto_docs(
    "api/v1/i2v",
    "POST",
    description="Роутер для получения статуса генерации.",
    params={
        "generation_id": {
            "type": "integer",
            "description": "Уникальный индефикатор генерации.",
        },
    },
)
async def generation_status(
    body: StatusBody,
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
    return await view.generation_status(
        body,
    )
