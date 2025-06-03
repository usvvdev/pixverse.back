# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)

from ...views.v1 import PixverseStyleView

from .....domain.tools import auto_docs, validate_token

from ....factroies.api.v1 import PixverseStyleViewFactory

from .....interface.schemas.api import Style


style_router = APIRouter(tags=["Styles"])


@style_router.get(
    "/styles",
)
async def fetch_styles(
    _: str = Depends(validate_token),
    view: PixverseStyleView = Depends(PixverseStyleViewFactory.create),
) -> list[Style]:
    return await view.fetch_styles()


@style_router.get(
    "/style/{template_id}",
)
async def fetch_style_by_template_id(
    template_id: int,
    _: str = Depends(validate_token),
    view: PixverseStyleView = Depends(PixverseStyleViewFactory.create),
) -> Style:
    return await view.fetch_style_by_template_id(
        template_id,
    )


@style_router.get(
    "/style/{id}",
)
async def fetch_style_by_id(
    id: int,
    _: str = Depends(validate_token),
    view: PixverseStyleView = Depends(PixverseStyleViewFactory.create),
) -> Style:
    return await view.fetch_style_by_id(
        id,
    )


@style_router.post(
    "/style",
)
async def add_style(
    data: Style,
    _: str = Depends(validate_token),
    view: PixverseStyleView = Depends(PixverseStyleViewFactory.create),
) -> Style:
    return await view.add_style(
        data,
    )


@style_router.put(
    "/style/{id}",
)
async def update_style(
    id: int,
    data: Style,
    _: str = Depends(validate_token),
    view: PixverseStyleView = Depends(PixverseStyleViewFactory.create),
) -> Style:
    return await view.update_style(
        id,
        data,
    )


@style_router.delete(
    "/style/{id}",
)
async def delete_style(
    id: int,
    _: str = Depends(validate_token),
    view: PixverseStyleView = Depends(PixverseStyleViewFactory.create),
) -> Style:
    return await view.delete_style(
        id,
    )
