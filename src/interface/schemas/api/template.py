# coding utf-8

from typing import Annotated

from pydantic import Field

from ....domain.entities.core import ISchema


class ITemplate(ISchema):
    prompt: Annotated[
        str,
        Field(...),
    ]
    name: Annotated[
        str,
        Field(...),
    ]
    category: Annotated[
        str,
        Field(...),
    ]


class ChangeTemplate(ITemplate):
    preview_small: Annotated[
        str | None,
        Field(default=None),
    ]
    preview_large: Annotated[
        str | None,
        Field(default=None),
    ]
    is_active: Annotated[
        bool,
        Field(default=True),
    ]


class Template(ChangeTemplate):
    id: Annotated[
        int,
        Field(...),
    ]
    template_id: Annotated[
        int | None,
        Field(default=None),
    ]
