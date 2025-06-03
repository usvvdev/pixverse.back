# coding utf-8

from typing import Annotated, Any

from pydantic import (
    Field,
    computed_field,
)

from ....domain.entities.core import ISchema


class StatusRes(ISchema):
    video_id: Annotated[
        int,
        Field(...),
    ]
    video_status: Annotated[
        int,
        Field(...),
    ]
    first_frame: Annotated[
        str,
        Field(...),
    ]
    url: Annotated[
        str,
        Field(...),
    ]


class TemplateResp(ISchema):
    restyle_id: Annotated[
        int,
        Field(...),
    ]
    display_name: Annotated[
        str,
        Field(...),
    ]
    restyle_prompt: Annotated[
        str,
        Field(...),
    ]


class ItemsResponse(ISchema):
    items: Annotated[
        list[TemplateResp],
        Field(...),
    ]


class TokensResponse(ISchema):
    credit_daily: Annotated[
        int,
        Field(default=0, exclude=True),
    ]
    credit_monthly: Annotated[
        int,
        Field(default=0, exclude=True),
    ]
    credit_package: Annotated[
        int,
        Field(default=0, exclude=True),
    ]

    @computed_field
    @property
    def credits(
        self,
    ) -> int:
        return sum(
            (
                self.credit_daily,
                self.credit_monthly,
                self.credit_package,
            )
        )


class AuthRes(ISchema):
    access_token: Annotated[
        str,
        Field(..., alias="Token"),
    ]


class ResResp(ISchema):
    result: Annotated[
        AuthRes,
        Field(..., alias="Result"),
    ]


class Resp(ISchema):
    video_id: Annotated[
        int,
        Field(...),
    ]
    detail: Annotated[
        str,
        Field(default="Success"),
    ]


class StatusResp(ISchema):
    data: Annotated[
        list[StatusRes],
        Field(...),
    ]


class GenerationStatus(ISchema):
    status: Annotated[
        str,
        Field(...),
    ]
    video_url: Annotated[
        str | None,
        Field(default=None),
    ]


class Effect(ISchema):
    display_name: Annotated[
        str,
        Field(...),
    ]
    template_id: Annotated[
        int,
        Field(...),
    ]


class FrameResp(ISchema):
    last_frame: Annotated[
        str,
        Field(...),
    ]


class ChannelItem(ISchema):
    channel_id: Annotated[
        int,
        Field(...),
    ]
    channel_name: Annotated[
        str,
        Field(...),
    ]
    effect_items: Annotated[
        list[Effect],
        Field(...),
    ]


class EffectResponse(ISchema):
    effect_channel_items: Annotated[
        list[ChannelItem],
        Field(...),
    ]


class UTResp(ISchema):
    Ak: Annotated[
        str,
        Field(..., alias="access_key_id"),
    ]
    Sk: Annotated[
        str,
        Field(..., alias="access_key_secret"),
    ]
    Token: Annotated[
        str,
        Field(..., alias="security_token"),
    ]


class Response(ISchema):
    err_code: Annotated[
        int,
        Field(..., alias="ErrCode"),
    ]
    err_msg: Annotated[
        str | None,
        Field(default=None, alias="ErrMsg"),
    ]
    resp: Annotated[
        Resp
        | ItemsResponse
        | EffectResponse
        | UTResp
        | FrameResp
        | ResResp
        | StatusResp
        | TokensResponse
        | Any,
        Field(default=None, alias="Resp"),
    ]
