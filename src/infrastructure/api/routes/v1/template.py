# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ...views.v1 import PixverseTemplateView

from .....domain.tools import auto_docs, validate_token

from ....factroies.api.v1 import PixverseTemplateViewFactory

from .....interface.schemas.api import Template


template_router = APIRouter(tags=["Templates"])


@template_router.get(
    "/templates",
)
async def fetch_templates(
    _: str = Depends(validate_token),
    view: PixverseTemplateView = Depends(PixverseTemplateViewFactory.create),
) -> list[Template]:
    return await view.fetch_templates()


@template_router.get(
    "/template/{template_id}",
)
async def fetch_template_by_template_id(
    template_id: int,
    _: str = Depends(validate_token),
    view: PixverseTemplateView = Depends(PixverseTemplateViewFactory.create),
) -> Template:
    return await view.fetch_template_by_template_id(
        template_id,
    )


@template_router.get(
    "/template/{id}",
)
async def fetch_template_by_id(
    id: int,
    _: str = Depends(validate_token),
    view: PixverseTemplateView = Depends(PixverseTemplateViewFactory.create),
) -> Template:
    return await view.fetch_template_by_id(
        id,
    )


@template_router.post(
    "/template",
)
async def add_template(
    data: Template,
    _: str = Depends(validate_token),
    view: PixverseTemplateView = Depends(PixverseTemplateViewFactory.create),
) -> Template:
    return await view.add_template(
        data,
    )


@template_router.put(
    "/template/{id}",
)
async def update_template(
    id: int,
    data: Template,
    _: str = Depends(validate_token),
    view: PixverseTemplateView = Depends(PixverseTemplateViewFactory.create),
) -> Template:
    return await view.update_template(
        id,
        data,
    )


@template_router.delete(
    "/template/{id}",
)
async def delete_template(
    id: int,
    _: str = Depends(validate_token),
    view: PixverseTemplateView = Depends(PixverseTemplateViewFactory.create),
) -> Template:
    return await view.delete_template(
        id,
    )
