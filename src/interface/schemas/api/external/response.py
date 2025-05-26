# coding utf-8

from typing import Annotated, Any

from pydantic import Field

from .....domain.entities import ISchema


class ResultImage(ISchema):
    img_id: Annotated[
        int,
        Field(...),
    ]
    img_url: Annotated[
        str,
        Field(...),
    ]


class ResultAuth(ISchema):
    account_id: Annotated[
        int,
        Field(..., alias="AccountId"),
    ]
    username: Annotated[
        str,
        Field(..., alias="Username"),
    ]
    token: Annotated[
        str,
        Field(..., alias="Token"),
    ]
    delete_at: Annotated[
        str,
        Field(..., alias="DeleteAt"),
    ]


class ResultT2V(ISchema):
    success_count: Annotated[
        int,
        Field(...),
    ]
    total_count: Annotated[
        int,
        Field(...),
    ]
    video_id: Annotated[
        int,
        Field(...),
    ]
    video_ids: Annotated[
        list[int],
        Field(...),
    ]


class ResultStatus(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
    prompt: Annotated[
        str,
        Field(...),
    ]
    url: Annotated[
        str,
        Field(...),
    ]
    size: Annotated[
        int,
        Field(...),
    ]
    status: Annotated[
        int,
        Field(...),
    ]


class Response(ISchema):
    result: Annotated[
        ResultImage | ResultAuth | ResultT2V,
        Field(..., alias="Result"),
    ]


class ResponseModel(ISchema):
    err_code: Annotated[
        int,
        Field(..., alias="ErrCode"),
    ]
    err_msg: Annotated[
        str | None,
        Field(default=None, alias="ErrMsg"),
    ]
    response: Annotated[
        Response | ResultStatus | ResultImage | Any,
        Field(default=None, alias="Resp"),
    ]
