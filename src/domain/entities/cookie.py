# coding utf-8

from typing import Annotated

from pydantic import Field

from .base import ISchema


class ICookie(ISchema):
    name: Annotated[
        str,
        Field(default="ai_token"),
    ]
    value: Annotated[
        str,
        Field(...),
    ]
