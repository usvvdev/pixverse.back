# coding utf-8

from typing import Annotated

from pydantic import Field

from ....domain.entities.core import ISchema


class Template(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
    template_id: Annotated[
        int | None,
        Field(default=None),
    ]
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
    preview: Annotated[
        str,
        Field(...),
    ]
