# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ....views.v1 import UserDataView

from ......domain.tools import auto_docs

from .....factroies.api.v1 import UserDataViewFactory

from ......interface.schemas.external import UserStatistics


user_data_router = APIRouter(tags=["User Data"])


@user_data_router.get(
    "/statistics",
)
@auto_docs(
    "api/v1/statistics",
    "GET",
    description="Роутер для получения стастистики по пользователям.",
)
async def fetch_user_data(
    view: UserDataView = Depends(UserDataViewFactory.create),
) -> list[UserStatistics]:
    return await view.fetch_user_data()
