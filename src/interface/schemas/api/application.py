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
    styles: Annotated[
        list[Style] | None,
        Field(default=None),
    ]

    @field_validator(
        "styles",
        mode="before",
    )
    @classmethod
    def validate_styles(
        cls,
        value: list,
    ) -> list[Style] | None:
        if len(value) > 0:
            return value
        return None


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
