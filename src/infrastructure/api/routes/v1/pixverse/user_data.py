# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ....views.v1 import UserDataView

# from ......domain.tools import auto_docs

from .....factroies.api.v1 import UserDataViewFactory

from ......interface.schemas.api import UserData


user_data_router = APIRouter(tags=["User Data"])


@user_data_router.get(
    "/userdata",
    # include_in_schema=False,
)
async def fetch_user_data(
    view: UserDataView = Depends(UserDataViewFactory.create),
) -> list[UserData]:
    return await view.fetch_user_data()
