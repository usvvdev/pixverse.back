# coding utf-8

from typing import Annotated

from pydantic import Field, field_validator

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


class PhotoGeneratorApplication(IApplication):
    pass


class PixverseApplication(IApplication):
    styles: Annotated[
        list[Style] | list,
        Field(default=[]),
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


class Application(PixverseApplication):
    id: Annotated[
        int,
        Field(...),
    ]
