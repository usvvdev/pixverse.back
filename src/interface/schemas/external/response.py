# coding utf-8

from typing import Annotated, Any

from os import getenv

from json import loads

from pendulum import now

from pydantic import (
    Field,
    field_validator,
    computed_field,
    HttpUrl,
)

from instagrapi import Client

from instagrapi.types import (
    User,
    Media,
)

from ....domain.conf import app_conf

from ....domain.entities.core import (
    ISchema,
    IConfEnv,
)


app_service: str = f"/{getenv('APP_SERVICE', 'default')}"

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
        if value is None:
            return value
        relative_path = value.removeprefix("uploads/")
        return f"{conf.domain_url}{app_service}{conf.api_prefix}/media/{relative_path}"


class IInstagramResponse(ISchema):
    username: Annotated[
        str,
        Field(...),
    ]
    datetime: Annotated[
        str,
        Field(default_factory=lambda: str(now())),
    ]
    status: Annotated[
        str,
        Field(default="success"),
    ]
    detail: Annotated[
        str,
        Field(...),
    ]


class InstagramSessionResponse(IInstagramResponse):
    detail: Annotated[
        str,
        Field(default="Session has been loaded"),
    ]


class InstagramAuthResponse(IInstagramResponse):
    detail: Annotated[
        str,
        Field(default="Succesfull authorization and session has been saved"),
    ]


class InstagramUserStatistics(ISchema):
    follower_count: Annotated[
        int,
        Field(..., alias="followers"),
    ]
    following_count: Annotated[
        int,
        Field(..., alias="subscribtions"),
    ]
    media_count: Annotated[
        int,
        Field(..., alias="publications"),
    ]
    likes_count: Annotated[
        int,
        Field(..., alias="likes"),
    ]
    comments_count: Annotated[
        int,
        Field(..., alias="comments"),
    ]
    mutual: Annotated[
        int,
        Field(...),
    ]
    not_following_you: Annotated[
        int,
        Field(...),
    ]
    not_followed_by_you: Annotated[
        int,
        Field(...),
    ]

    @classmethod
    def from_data(
        cls,
        user: User,
        client: Client,
        medias: list[Media],
    ) -> "InstagramUserStatistics":
        following = set(
            client.user_following(user.pk).keys(),
        )
        followers = set(
            client.user_followers(user.pk).keys(),
        )
        return cls(
            **user.model_dump(),
            likes_count=sum(m.like_count for m in medias),
            comments_count=sum(m.comment_count for m in medias),
            mutual=len(following & followers),
            not_following_you=len(following - followers),
            not_followed_by_you=len(followers - following),
        )


class InstagramPost(ISchema):
    id: Annotated[
        str,
        Field(...),
    ]
    view_count: Annotated[
        int,
        Field(..., alias="views"),
    ]
    like_count: Annotated[
        int,
        Field(..., alias="likes"),
    ]
    comment_count: Annotated[
        int,
        Field(..., alias="comments"),
    ]
    thumbnail_url: Annotated[
        HttpUrl | None,
        Field(default=None),
    ]

    @classmethod
    def from_medias(
        cls,
        medias: list[Media],
    ) -> list["InstagramPost"]:
        return list(
            map(
                lambda m: cls(
                    **m.model_dump(),
                ),
                medias,
            )
        )


class InstagramUser(ISchema):
    username: Annotated[
        str,
        Field(...),
    ]
    full_name: Annotated[
        str,
        Field(...),
    ]
    biography: Annotated[
        str | None,
        Field(default=None),
    ]
    profile_pic_url: Annotated[
        HttpUrl,
        Field(...),
    ]
    is_private: Annotated[
        bool,
        Field(...),
    ]
    is_verified: Annotated[
        bool,
        Field(...),
    ]

    @classmethod
    def from_user(
        cls,
        user: User,
    ) -> "InstagramUser":
        return cls(
            **user.model_dump(),
        )


class InstagramUserResponse(ISchema):
    user: Annotated[
        InstagramUser,
        Field(...),
    ]
    statistics: Annotated[
        InstagramUserStatistics,
        Field(...),
    ]
    posts: Annotated[
        list[InstagramPost],
        Field(...),
    ]


class InstagramFollower(ISchema):
    username: Annotated[
        str,
        Field(...),
    ]
    full_name: Annotated[
        str,
        Field(...),
    ]
    profile_pic_url: Annotated[
        HttpUrl | None,
        Field(default=None),
    ]


class ChatGPTCosmetic(ISchema):
    title: Annotated[
        str,
        Field(...),
    ]
    description: Annotated[
        str,
        Field(...),
    ]
    purpose: Annotated[
        str,
        Field(...),
    ]


class ChatGPTCosmeticMessage(ISchema):
    content: Annotated[
        list[ChatGPTCosmetic],
        Field(...),
    ]

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(
        cls,
        value,
    ) -> Any:
        return loads(value)


class ChatGPTCosmeticChoice(ISchema):
    index: Annotated[
        int,
        Field(...),
    ]
    message: Annotated[
        ChatGPTCosmeticMessage,
        Field(...),
    ]


class ChatGPTCosmeticResponse(ISchema):
    choices: Annotated[
        list[ChatGPTCosmeticChoice],
        Field(...),
    ]

    def fetch_data(
        self,
    ) -> list[ChatGPTCosmetic]:
        return self.choices[0].message.content
