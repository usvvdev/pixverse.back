# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    File,
)


from ...views.v1 import PixVerseView

from .....domain.tools import auto_docs

from .....interface.schemas.external import (
    T2VBody,
    I2VBody,
    R2VBody,
    Resp,
    GenerationStatus,
    TE2VBody,
)

from ....factroies.api.v1 import PixVerseViewFactory


pixverse_router = APIRouter(tags=["Pixverse"])


@pixverse_router.post(
    "/text2video",
    response_model=Resp,
    response_model_exclude_none=True,
)
@auto_docs(
    "api/v1/text2video",
    "POST",
    description="Роутер для создания видео по загруженой фотографии и параметрам.",
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
async def text_to_video(
    body: T2VBody = Depends(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
    """
    Генерирует видео на основе текстового запроса.

    Аргументы:
        body (IBody): Тело запроса, содержащее текст (prompt) и дополнительные параметры.
        token (str): OAuth2 access token для авторизации пользователя.
        view (PixVerseView): Зависимость, обрабатывающая бизнес-логику генерации видео.

    Возвращает:
        ResponseModel: Ответ с данными о результате генерации видео.
    """
    return await view.text_to_video(
        body,
    )


@pixverse_router.post(
    "/image2video",
    response_model=Resp,
    response_model_exclude_none=True,
)
@auto_docs(
    "api/v1/image2video",
    "POST",
    description="Роутер для создания видео по загруженой фотографии и параметрам.",
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
        "image": {
            "type": "bytes",
            "description": "Фотография для обработки",
        },
    },
)
async def image_to_video(
    body: I2VBody = Depends(),
    image: UploadFile = File(...),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
    return await view.image_to_video(
        body,
        image,
    )


@pixverse_router.post(
    "/video2video",
    response_model=Resp,
    response_model_exclude_none=True,
)
@auto_docs(
    "api/v1/video2video",
    "POST",
    description="Роутер для создания видео по загруженой фотографии и параметрам.",
    params={
        "userId": {
            "type": "string",
            "description": "Уникальный идентификатор пользователя",
        },
        "appId": {
            "type": "string",
            "description": "Уникальный идентификатор приложения",
        },
        "templateId": {
            "type": "integer",
            "description": "Уникальный идентификатор стиля",
        },
        "video": {
            "type": "bytes",
            "description": "Видео-фрагмент для обработки",
        },
    },
)
async def restyle_video(
    body: R2VBody = Depends(),
    video: UploadFile = File(...),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
    return await view.restyle_video(
        body,
        video,
    )


@pixverse_router.post(
    "/template2video",
    response_model=Resp,
    response_model_exclude_none=True,
)
@auto_docs(
    "api/v1/template2video",
    "POST",
    description="Роутер для создания видео по загруженой фотографии и параметрам.",
    params={
        "userId": {
            "type": "string",
            "description": "Уникальный идентификатор пользователя",
        },
        "appId": {
            "type": "string",
            "description": "Уникальный идентификатор приложения",
        },
        "templateId": {
            "type": "integer",
            "description": "Уникальный идентификатор стиля",
        },
        "images": {
            "type": "bytes",
            "description": "Фотография для обработки",
        },
    },
)
async def template_video(
    body: TE2VBody = Depends(),
    image: UploadFile = File(...),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
    return await view.template_video(
        body,
        image,
    )


@pixverse_router.get(
    "/status",
)
@auto_docs(
    "api/v1/status/{id}",
    "POST",
    description="Роутер для получения статуса генерации.",
    params={
        "id": {
            "type": "integer",
            "description": "Уникальный индефикатор генерации.",
        },
    },
)
async def generation_status(
    id: int,
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> GenerationStatus:
    """
    Получение текущего статуса генерации видео.

    Аргументы:
        body (GenBody): Тело запроса с параметрами генерации.
            Обязательные поля:
            - video_id (int): Уникальный идентификатор задачи генерации
        token (str): OAuth2 токен доступа для аутентификации пользователя.
            Автоматически внедряется через dependency injection.
        view (PixVerseView): Экземпляр обработчика бизнес-логики.
            Автоматически создается через фабрику зависимостей.

    Возвращает:
        GenerationStatus: Объект с информацией о статусе генерации
    """
    return await view.generation_status(
        id,
    )
