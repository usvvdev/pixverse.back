# coding utf-8

from typing import Annotated

from pydantic import Field

from .template import Template

from .style import Style

from ....domain.entities.core import ISchema


class IApplication(ISchema):
    app_id: Annotated[
        str,
        Field(...),
    ]
    templates: Annotated[
        list[Template] | None,
        Field(default=None),
    ]
    styles: Annotated[
        list[Style] | None,
        Field(default=None),
    ]


class ChangeApplication(ISchema):
    app_id: Annotated[
        str,
        Field(...),
    ]
    template_ids: Annotated[
        list[int],
        Field(...),
    ]
    style_ids: Annotated[
        list[int],
        Field(...),
    ]


class Application(IApplication):
    id: Annotated[
        int,
        Field(...),
    ]
