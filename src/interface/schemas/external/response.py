# coding utf-8

from typing import Annotated, Any

from json import loads

from pydantic import (
    Field,
    field_validator,
    computed_field,
)

from ....domain.conf import app_conf

from ....domain.entities.core import (
    ISchema,
    IConfEnv,
)


conf: IConfEnv = app_conf()


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
    prompt: Annotated[
        str,
        Field(..., alias="display_prompt"),
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


class ChatGPTData(ISchema):
    b64_json: Annotated[
        str,
        Field(...),
    ]


class ChatGPTError(ISchema):
    code: Annotated[
        str | None,
        Field(default=None),
    ]
    message: Annotated[
        str,
        Field(...),
    ]


class ICalories(ISchema):
    title: Annotated[
        str,
        Field(...),
    ]
    kilocalories_per100g: Annotated[
        float,
        Field(...),
    ]
    proteins_per100g: Annotated[
        float,
        Field(...),
    ]
    fats_per100g: Annotated[
        float,
        Field(...),
    ]
    carbohydrates_per100g: Annotated[
        float,
        Field(...),
    ]
    fiber_per100g: Annotated[
        float,
        Field(...),
    ]


class CaloriesItems(ICalories):
    weight: Annotated[
        int,
        Field(...),
    ]


class ChatGPTCalories(ISchema):
    items: Annotated[
        list[CaloriesItems],
        Field(...),
    ]
    total: Annotated[
        ICalories,
        Field(...),
    ]


class ChatGPTCaloriesMessage(ISchema):
    content: Annotated[
        ChatGPTCalories,
        Field(...),
    ]

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(
        cls,
        value,
    ) -> Any:
        return loads(value)


class ChatGPTCaloriesChoice(ISchema):
    index: Annotated[
        int,
        Field(...),
    ]
    message: Annotated[
        ChatGPTCaloriesMessage,
        Field(...),
    ]


class ChatGPTCaloriesResponse(ISchema):
    choices: Annotated[
        list[ChatGPTCaloriesChoice],
        Field(...),
    ]

    def fetch_data(
        self,
    ) -> ChatGPTCalories:
        return self.choices[0].message.content


class ChatGPTErrorResponse(ISchema):
    error: Annotated[
        ChatGPTError,
        Field(...),
    ]


class ChatGPTResponse(ISchema):
    created: Annotated[
        int,
        Field(...),
    ]
    background: Annotated[
        str,
        Field(...),
    ]
    data: Annotated[
        list[ChatGPTData],
        Field(...),
    ]
    output_format: Annotated[
        str,
        Field(...),
    ]
    quality: Annotated[
        str,
        Field(...),
    ]
    size: Annotated[
        str,
        Field(...),
    ]


class ChatGPTResp(ISchema):
    url: Annotated[
        str,
        Field(...),
    ]
    detail: Annotated[
        str,
        Field(default="Success"),
    ]

    @field_validator("url", mode="after")
    @classmethod
    def create_preview_large_url(
        cls,
        value: str,
    ) -> str:
        return (
            "".join((conf.domain_url, value.replace("uploads/", "/static/")))
            if value is not None
            else value
        )
