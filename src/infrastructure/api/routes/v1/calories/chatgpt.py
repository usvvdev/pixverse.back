# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    File,
)

from ....views.v1 import CaloriesView

from ......domain.tools import auto_docs

from ......domain.entities.chatgpt import (
    T2CBody,
    I2CBody,
)

from .....factroies.api.v1 import CaloriesViewFactory

from ......interface.schemas.external import ChatGPTCalories


calories_router = APIRouter(tags=["Calories"])


@calories_router.post(
    "/text2calories",
)
@auto_docs(
    "api/v1/text2calories",
    "POST",
    params={
        "userId": {
            "type": "string",
            "description": "Уникальный идентификатор пользователя",
        },
        "appId": {
            "type": "string",
            "description": "Уникальный идентификатор приложения",
        },
        "description": {
            "type": "string",
            "description": "Описание блюда для получения бжу",
        },
    },
    description="Роутер для получения бжу по описанию блюда",
)
async def text_to_calories(
    body: T2CBody = Depends(),
    view: CaloriesView = Depends(CaloriesViewFactory.create),
) -> ChatGPTCalories:
    return await view.text_to_calories(
        body.description,
    )


@calories_router.post(
    "/photo2calories",
)
@auto_docs(
    "api/v1/text2calories",
    "POST",
    params={
        "userId": {
            "type": "string",
            "description": "Уникальный идентификатор пользователя",
        },
        "appId": {
            "type": "string",
            "description": "Уникальный идентификатор приложения",
        },
        "image": {
            "type": "string",
            "description": "Медиа файл с изображением блюда",
        },
    },
    description="Роутер для получения бжу по изображению блюда",
)
async def photo_to_calories(
    body: I2CBody = Depends(),
    image: UploadFile = File(),
    view: CaloriesView = Depends(CaloriesViewFactory.create),
) -> ChatGPTCalories:
    return await view.photo_to_calories(
        image,
    )
