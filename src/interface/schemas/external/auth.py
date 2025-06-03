# codinng utf-8

from typing import Annotated

from pydantic import Field

from ....domain.conf import app_conf

from ....domain.entities.core import (
    ISchema,
    IConfEnv,
)


conf: IConfEnv = app_conf()


class UserCredentials(ISchema):
    username: Annotated[
        str,
        Field(default=conf.username, alias="Username"),
    ]
    password: Annotated[
        str,
        Field(default=conf.password, alias="Password"),
    ]


class AccessToken(ISchema):
    access_token: Annotated[
        str,
        Field(...),
    ]
