# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    File,
)

from json import loads

from ....views.v1 import CaloriesView

# from ......domain.tools import auto_docs

from .....factroies.api.v1 import CaloriesViewFactory


calories_router = APIRouter(tags=["Calories"])


@calories_router.post(
    "/text2calories",
)
async def text_to_calories(
    description: str,
    view: CaloriesView = Depends(CaloriesViewFactory.create),
):
    response = await view.text_to_calories(
        description,
    )
    return {"response": loads(response)}


@calories_router.post(
    "/photo2calories",
)
async def photo_to_calories(
    image: UploadFile = File(),
    view: CaloriesView = Depends(CaloriesViewFactory.create),
):
    response = await view.photo_to_calories(
        image,
    )
    return {"response": loads(response)}
