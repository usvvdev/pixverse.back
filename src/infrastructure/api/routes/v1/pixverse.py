# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
)

from pathlib import Path

from tempfile import NamedTemporaryFile

from shutil import copyfileobj

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ...views.v1 import PixVerseView

from .....interface.schemas.api import (
    StatusBody,
    UserCredentials,
)

from .....domain.entities import IBody

from ....factroies.api.v1 import PixVerseViewFactory

from .....domain.tools import auto_docs

from .....interface.schemas.api import ResponseModel


pixverse_router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth")


@pixverse_router.post(
    "/auth",
)
async def auth_user(
    body: OAuth2PasswordRequestForm = Depends(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
):
    user: ResponseModel = await view.auth_user(
        UserCredentials(
            **body.__dict__,
        ),
    )
    return {"access_token": user.response.result.token}


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
    body: IBody = Depends(),
    token: str = Depends(oauth2_scheme),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> ResponseModel:
    return await view.text_to_video(
        token,
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
    body: IBody = Depends(),
    token: str = Depends(oauth2_scheme),
    file: UploadFile = File(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> ResponseModel:
    suffix = Path(file.filename).suffix

    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        copyfileobj(file.file, tmp)
        tmp_path = Path(tmp.name).resolve()

    return await view.image_to_video(
        body,
        token,
        tmp_path,
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
    body: StatusBody = Depends(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> ResponseModel:
    return await view.generation_status(
        body,
    )
