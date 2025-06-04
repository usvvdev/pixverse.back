# coding utf-8

from typing import Annotated

from pydantic import Field

from ....domain.entities.core import ISchema


class IAccount(ISchema):
    username: Annotated[
        str,
        Field(...),
    ]
    password: Annotated[
        str,
        Field(...),
    ]


class ChangeAccount(IAccount):
    is_active: Annotated[
        bool,
        Field(default=1),
    ]
    balance: Annotated[
        int,
        Field(default=0),
    ]


class Account(ChangeAccount):
    id: Annotated[
        int,
        Field(...),
    ]
