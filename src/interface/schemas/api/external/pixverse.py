# coding utf-8

from typing import Annotated, Any

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
        Field(default="v4.5"),
    ]
    quality: Annotated[
        str,
        Field(default="360p"),
    ]


class TextBody(BaseBody):
    aspect_ratio: Annotated[
        str,
        Field(default="16:9"),
    ]
    credit_change: Annotated[
        int,
        Field(default=20),
    ]
    lip_sync_tts_speaker_id: Annotated[
        str,
        Field(default="Auto"),
    ]
    motion_mode: Annotated[
        str,
        Field(default="normal"),
    ]


class ImageBody(BaseBody):
    img_id: Annotated[
        int,
        Field(...),
    ]
    img_url: Annotated[
        str,
        Field(..., alias="customer_img_url"),
    ]
    img_path: Annotated[
        str,
        Field(
            default="upload/d0a7be74-b235-4d9c-978a-0abaaf2315ca.jpg",
            alias="customer_img_path",
        ),
    ]
    motion_mode: Annotated[
        str,
        Field(default="normal"),
    ]
    credit_change: Annotated[
        int,
        Field(default=20),
    ]
    lip_sync_tts_speaker_id: Annotated[
        str,
        Field(default="Auto"),
    ]


class StatusBody(ISchema):
    generation_id: Annotated[
        int,
        Field(...),
    ]


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


class UserCredentials(ISchema):
    username: Annotated[
        str,
        Field(..., alias="Username"),
    ]
    password: Annotated[
        str,
        Field(..., alias="Password"),
    ]
