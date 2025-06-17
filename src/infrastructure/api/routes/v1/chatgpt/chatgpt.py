# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    File,
)

from ......interface.schemas.external.response import ChatGPTResp

from ....views.v1 import ChatGPTView

from ......domain.tools import auto_docs

from ......domain.entities.chatgpt import IBody, T2PBody

from .....factroies.api.v1 import ChatGPTViewFactory


chatgpt_router = APIRouter(tags=["ChatGPT"])


@chatgpt_router.post(
    "/text2photo",
    response_model_exclude_none=True,
)
@auto_docs(
    "api/v1/text2photo",
    "POST",
    description="Роутер для создания фото по параметрам.",
    params={
        "promt": {
            "type": "string",
            "description": "Текст для создания видео фрагмента",
        },
        "userId": {
            "type": "string",
            "description": "Уникальный идентификатор пользователя",
        },
        "appId": {
            "type": "string",
            "description": "Уникальный идентификатор приложения",
        },
    },
)
async def text_to_photo(
    body: IBody = Depends(),
    view: ChatGPTView = Depends(ChatGPTViewFactory.create),
) -> ChatGPTResp:
    """
    Генерирует видео на основе текстового запроса.

    Аргументы:
        body (IBody): Тело запроса, содержащее текст (prompt) и дополнительные параметры.
        token (str): OAuth2 access token для авторизации пользователя.
        view (PixVerseView): Зависимость, обрабатывающая бизнес-логику генерации видео.

    Возвращает:
        ResponseModel: Ответ с данными о результате генерации видео.
    """
    return await view.text_to_photo(
        body,
    )


@chatgpt_router.post(
    "/photo2photo",
    response_model_exclude_none=True,
)
@auto_docs(
    "api/v1/photo2photo",
    "POST",
    description="Роутер для создания фото по загруженой фотографии и параметрам.",
    params={
        "promt": {
            "type": "string",
            "description": "Текст для создания видео фрагмента",
        },
        "userId": {
            "type": "string",
            "description": "Уникальный идентификатор пользователя",
        },
        "appId": {
            "type": "string",
            "description": "Уникальный идентификатор приложения",
        },
        "iamge": {
            "type": "bytes",
            "description": "Фотонрафия для приложения",
        },
    },
)
async def photo_to_photo(
    body: IBody = Depends(),
    image: UploadFile = File(),
    view: ChatGPTView = Depends(ChatGPTViewFactory.create),
):
    """
    Генерирует видео на основе текстового запроса.

    Аргументы:
        body (IBody): Тело запроса, содержащее текст (prompt) и дополнительные параметры.
        token (str): OAuth2 access token для авторизации пользователя.
        view (PixVerseView): Зависимость, обрабатывающая бизнес-логику генерации видео.

    Возвращает:
        ResponseModel: Ответ с данными о результате генерации видео.
    """
    return await view.photo_to_photo(
        body,
        image,
    )


@chatgpt_router.post(
    "/template2photo",
    response_model_exclude_none=True,
)
@auto_docs(
    "api/v1/template2photo",
    "POST",
    description="Роутер для фото по опреденному шаблону и фото.",
    params={
        "promt": {
            "type": "string",
            "description": "Текст для создания видео фрагмента",
        },
        "userId": {
            "type": "string",
            "description": "Уникальный идентификатор пользователя",
        },
        "appId": {
            "type": "string",
            "description": "Уникальный идентификатор приложения",
        },
        "tempalte_id": {
            "type": "integer",
            "description": "Уникальный идентификатор шаблона",
        },
    },
)
async def template_to_photo(
    body: T2PBody = Depends(),
    image: UploadFile = File(),
    view: ChatGPTView = Depends(ChatGPTViewFactory.create),
) -> ChatGPTResp:
    """
    Генерирует видео на основе текстового запроса.

    Аргументы:
        body (IBody): Тело запроса, содержащее текст (prompt) и дополнительные параметры.
        token (str): OAuth2 access token для авторизации пользователя.
        view (PixVerseView): Зависимость, обрабатывающая бизнес-логику генерации видео.

    Возвращает:
        ResponseModel: Ответ с данными о результате генерации видео.
    """
    return await view.template_to_photo(
        body,
        image,
    )
