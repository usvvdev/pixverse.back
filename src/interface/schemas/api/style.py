# coding utf-8

from typing import Annotated

from pydantic import Field

from ....domain.entities.core import ISchema


class IStyle(ISchema):
    prompt: Annotated[
        str,
        Field(...),
    ]
    name: Annotated[
        str,
        Field(...),
    ]


class ChangeStyle(IStyle):
    preview_small: Annotated[
        str | None,
        Field(default=None),
    ]
    preview_large: Annotated[
        str | None,
        Field(default=None),
    ]


class Style(ChangeStyle):
    id: Annotated[
        int,
        Field(...),
    ]
    template_id: Annotated[
        int | None,
        Field(default=None),
    ]
