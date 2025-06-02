# coding utf-8

from typing import Annotated

from pydantic import Field

from ....domain.entities.core import ISchema


class Account(ISchema):
    username: Annotated[
        str,
        Field(...),
    ]
    password: Annotated[
        str,
        Field(...),
    ]
