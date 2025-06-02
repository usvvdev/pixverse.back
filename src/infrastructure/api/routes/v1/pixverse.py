# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from ...views.v1 import PixVerseView

from .....domain.entities.pixverse import IBody

from .....domain.tools import auto_docs

from .....interface.schemas.external import (
    T2VBody,
    AuthRes,
    Resp,
    GenBody,
    TemplateBody,
    TokensResponse,
    GenerationStatus,
    Template,
    EffectResponse,
)

from ....factroies.api.v1 import PixVerseViewFactory


pixverse_router = APIRouter(tags=["Pixverse"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth")


@pixverse_router.post(
    "/auth",
)
async def auth_user(
    body: OAuth2PasswordRequestForm = Depends(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> AuthRes:
    """
    Выполняет аутентификацию пользователя и выдает access token.

    Аргументы:
        body (OAuth2PasswordRequestForm): Форма с логином и паролем (username и password).
        view (PixVerseView): Экземпляр представления, обрабатывающий бизнес-логику аутентификации.

    Возвращает:
        AccessToken: Токен доступа, который можно использовать для авторизованных запросов.
    """
    return await view.auth_user(
        body,
    )


@pixverse_router.post(
    "/t2v",
    response_model=Resp,
    response_model_exclude_none=True,
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
async def text_to_video(
    body: T2VBody,
    token: str = Depends(oauth2_scheme),
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
        token,
    )


@pixverse_router.post(
    "/i2v",
    response_model=Resp,
    response_model_exclude_none=True,
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
    body: IBody = Depends(),  # TODO -- подумать, как лучше
    image: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
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
        body,
        image,
        token,
    )


@pixverse_router.post(
    "/status",
)
@auto_docs(
    "api/v1/status",
    "POST",
    description="Роутер для получения статуса генерации.",
    params={
        "video_id": {
            "type": "integer",
            "description": "Уникальный индефикатор генерации.",
        },
    },
)
async def generation_status(
    body: GenBody,
    token: str = Depends(oauth2_scheme),
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
        body,
        token,
    )


@pixverse_router.get(
    "/credits",
)
@auto_docs(
    "api/v1/credits",
    "GET",
    description="Роутер для получения баланса аккаунта.",
    params={
        "token": {
            "type": "string",
            "description": "JWT токен для идентификации аккаунта.",
        },
    },
)
async def credits_amount(
    token: str = Depends(oauth2_scheme),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> TokensResponse:
    """
    Получение текущего баланса кредитов пользователя.

    Аргументы:
        token (str): JWT токен доступа для аутентификации пользователя.
            Передается в заголовке Authorization: Bearer <token>.
            Автоматически валидируется через oauth2_scheme.
        view (PixVerseView): Экземпляр сервисного слоя для работы с балансом.
            Автоматически создается через фабрику зависимостей.

    Возвращает:
        TokensResponse: Объект с информацией о балансе токенов.
    """
    return await view.credits_amount(
        token,
    )


@pixverse_router.post(
    "/templates",
)
@auto_docs(
    "api/v1/templates",
    "POST",
    description="Роутер для получения стилей для конвертации видео.",
    params={
        "offset": {
            "type": "integer",
            "description": "Сдвиг по стилям.",
        },
        "limit": {
            "type": "integer",
            "description": "Ограничение по показу стилей по пагинации.",
        },
    },
)
async def restyle_templates(
    body: TemplateBody,
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> list[Template]:
    """
    Получение списка доступных стилей для преобразования видео.

    Аргументы:
        body (TemplateBody): Тело запроса с параметрами пагинации.
            Поля:
            - offset (int): Сдвиг в списке стилей (по умолчанию 0)
            - limit (int): Количество возвращаемых стилей (по умолчанию 20)
        view (PixVerseView): Сервис для работы с шаблонами стилей.
            Автоматически внедряется через DI.

    Возвращает:
        list[Template]: Список объектов с шаблонами.
    """
    return await view.restyle_templates(
        body,
    )


@pixverse_router.get(
    "/effects",
)
@auto_docs(
    "api/v1/templates",
    "GET",
    description="Роутер для получения эффектов для конвертации.",
)
async def effect_templates(
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> EffectResponse:
    """
    Получение списка доступных визуальных эффектов для видео.

    Аргументы:
        view (PixVerseView): Сервис для работы с эффектами.
            Автоматически внедряется через DI.

    Возвращает:
        EffectResponse: Объект с группированными эффектами:
    """
    return await view.effect_templates()
