# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    File,
)

from ....views.v1 import CosmeticView

from ......domain.tools import auto_docs

from ......domain.entities.chatgpt import (
    T2CBody,
    I2CBody,
)

from .....factroies.api.v1 import CosmeticViewFactory

from ......interface.schemas.external import ChatGPTCosmetic


cosmetic_router = APIRouter(tags=["Calories"])


@cosmetic_router.post(
    "/photo2cosmetic",
)
@auto_docs(
    "api/v1/photo2cosmetic",
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
            "description": "Медиа файл с изображением косметики",
        },
    },
    description="Роутер для получения описания косметки по фото",
)
async def photo_to_cosmetic(
    body: I2CBody = Depends(),
    image: UploadFile = File(),
    view: CosmeticView = Depends(CosmeticViewFactory.create),
) -> list[ChatGPTCosmetic]:
    return await view.photo_to_cosmetic(
        image,
    )
