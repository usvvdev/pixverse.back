# coding utf-8

from typing import Annotated

from pydantic import Field

from .....domain.entities import (
    IBody,
    ISchema,
)


class BaseBody(IBody):
    duration: Annotated[
        int,
        Field(default=5),
    ]
    model: Annotated[
        str,
        Field(default="v3.5"),
    ]
    quality: Annotated[
        str,
        Field(default="540p"),
    ]


class TextBody(BaseBody):
    aspect_ratio: Annotated[
        str,
        Field(default="16:9"),
    ]


class ImageBody(BaseBody):
    img_id: Annotated[
        int,
        Field(...),
    ]


class StatusBody(ISchema):
    generation_id: Annotated[
        int,
        Field(...),
    ]


class Result(ISchema):
    img_id: Annotated[
        int,
        Field(...),
    ]
    img_url: Annotated[
        str,
        Field(...),
    ]


class Resp(ISchema):
    err_code: Annotated[
        int,
        Field(..., alias="ErrCode"),
    ]
    err_msg: Annotated[
        str | None,
        Field(..., alias="ErrMsg"),
    ]
    res: Annotated[
        Result | None,
        Field(..., alias="Resp"),
    ]
