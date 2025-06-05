# coding utf-8

from typing import Annotated

from pydantic import Field

from .template import Template

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


class ChangeApplication(ISchema):
    app_id: Annotated[
        str,
        Field(...),
    ]
    ids: Annotated[
        list[int],
        Field(...),
    ]


class Application(IApplication):
    id: Annotated[
        int,
        Field(...),
    ]
