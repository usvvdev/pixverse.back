# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ....views.v1 import ApplicationView

from ......domain.tools import (
    validate_token,
)

from .....factroies.api.v1 import ApplicationViewFactory

from ......interface.schemas.api import (
    StoreApplication,
    ChangeStoreApplication,
    AddStoreApplication,
)


application_router = APIRouter(tags=["Appstore Applications"])


@application_router.get(
    "/store_applications",
)
async def fetch_applications(
    # _: str = Depends(validate_token),
    view: ApplicationView = Depends(
        ApplicationViewFactory.create,
    ),
) -> list[StoreApplication]:
    return await view.fetch_applications()


@application_router.get(
    "/store_applications/{id}",
)
async def fetch_application(
    id: int,
    _: str = Depends(validate_token),
    view: ApplicationView = Depends(
        ApplicationViewFactory.create,
    ),
) -> StoreApplication:
    return await view.fetch_application(
        id,
    )


@application_router.post(
    "/store_applications",
)
async def add_application(
    data: AddStoreApplication,
    # _: str = Depends(validate_token),
    view: ApplicationView = Depends(
        ApplicationViewFactory.create,
    ),
) -> AddStoreApplication:
    return await view.add_application(
        data,
    )


@application_router.put(
    "/store_applications/{id}",
)
async def update_application(
    id: int,
    data: ChangeStoreApplication,
    _: str = Depends(validate_token),
    view: ApplicationView = Depends(
        ApplicationViewFactory.create,
    ),
) -> ChangeStoreApplication:
    return await view.update_application(
        id,
        data,
    )


@application_router.delete(
    "/store_applications/{id}",
)
async def delete_application(
    id: int,
    _: str = Depends(validate_token),
    view: ApplicationView = Depends(
        ApplicationViewFactory.create,
    ),
) -> bool:
    return await view.delete_application(
        id,
    )
