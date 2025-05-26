# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
)

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from ...views.v1 import PixVerseView

from .....interface.schemas.api import (
    AccessToken,
    StatusBody,
)

from .....domain.entities import IBody

from .....domain.tools import auto_docs

from .....domain.errors import InvalidCredentials

from ....factroies.api.v1 import PixVerseViewFactory

from .....interface.schemas.api import ResponseModel


pixverse_router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth")


@pixverse_router.post(
    "/auth",
)
@auto_docs(
    "api/v1/t2v",
    "POST",
    description="Роутер для аунтефикации на платформе.",
    params={
        "username": {
            "type": "string",
            "description": "Имя аккаунта для авторизации",
        },
        "password": {
            "type": "string",
            "description": "Пароль для аккаунта авторизации",
        },
    },
)
async def auth_user(
    body: OAuth2PasswordRequestForm = Depends(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> AccessToken:
    """
    Выполняет аутентификацию пользователя и выдает access token.

    Аргументы:
        body (OAuth2PasswordRequestForm): Форма с логином и паролем (username и password).
        view (PixVerseView): Экземпляр представления, обрабатывающий бизнес-логику аутентификации.

    Возвращает:
        AccessToken: Токен доступа, который можно использовать для авторизованных запросов.
    """
    user: ResponseModel = await view.auth_user(
        body,
    )
    try:
        return AccessToken(
            access_token=user.response.result.token,
        )
    except (Exception, ValueError):
        raise InvalidCredentials


@pixverse_router.post(
    "/t2v",
)
@auto_docs(
    "api/v1/t2v",
    "POST",
    description="Роутер для создания видео по заданому тексту и параметрам.",
    params={
        "promt": {
            "type": "string",
            "description": "Текст для создания видео фрагмента",
        },
    },
)
async def text_to_video(
    body: IBody = Depends(),
    token: str = Depends(oauth2_scheme),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> ResponseModel:
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
        "promt": {
            "type": "string",
            "description": "Текст для создания видео фрагмента",
        },
    },
)
async def image_to_video(
    token: str = Depends(oauth2_scheme),
    body: IBody = Depends(),
    file: UploadFile = File(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> ResponseModel:
    """
    Генерирует видео на основе изображения и текстового описания.

    Аргументы:
        token (str): OAuth2 access token для авторизации пользователя.
        body (IBody): Данные с текстом (prompt) и дополнительными параметрами генерации.
        file (UploadFile): Загружаемое изображение, используемое в качестве основы для видео.
        view (PixVerseView): Экземпляр класса, содержащего бизнес-логику генерации.

    Возвращает:
        ResponseModel: Результат генерации видео.
    """
    return await view.image_to_video(
        token,
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
    body: StatusBody = Depends(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> ResponseModel:
    """
    Возвращает статус генерации видео по заданному идентификатору.

    Аргументы:
        body (StatusBody): Тело запроса, содержащее `generation_id`.
        view (PixVerseView): Зависимость с бизнес-логикой получения статуса.

    Возвращает:
        ResponseModel: Объект с текущим статусом генерации.
    """
    return await view.generation_status(
        body,
    )
