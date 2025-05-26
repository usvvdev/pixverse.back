# coding utf-8

from typing import Annotated

from pydantic import Field

from .....domain.entities import ISchema


class StatusBody(ISchema):
    generation_id: Annotated[
        int,
        Field(...),
    ]
