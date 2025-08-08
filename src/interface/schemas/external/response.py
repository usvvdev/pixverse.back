# coding utf-8

from typing import Annotated, Any, Literal

from os import getenv

from json import loads

from pendulum import now

from pydantic import (
    Field,
    field_validator,
    computed_field,
    model_validator,
    HttpUrl,
)

from datetime import date, datetime

from instaloader import Profile, Post

from time import sleep

from random import uniform

from instagrapi.types import (
    User,
    Media,
    UserShort,
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
    uuid: Annotated[
        str | None,
        Field(default=None),
    ]
    timestamp: Annotated[
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
        Field(default="Successfull authorization and session has been saved"),
    ]


class InstagramUpdateUserResponse(IInstagramResponse):
    detail: Annotated[
        str,
        Field(default="Successfull user data updation"),
    ]


class InstagramTrackingUserResponse(IInstagramResponse):
    detail: Annotated[
        str,
        Field(default="Successfull added user to tracking"),
    ]


class IInstagramUserStatistics(ISchema):
    id: Annotated[
        int | None,
        Field(default=None),
    ]
    likes_count: Annotated[
        int | None,
        Field(default=None),
    ]
    comments_count: Annotated[
        int | None,
        Field(default=None),
    ]
    publications_count: Annotated[
        int,
        Field(...),
    ]
    followers_count: Annotated[
        int,
        Field(...),
    ]
    following_count: Annotated[
        int,
        Field(...),
    ]
    mutual_subscriptions_count: Annotated[
        int | None,
        Field(default=None),
    ]
    non_reciprocal_following_count: Annotated[
        int | None,
        Field(default=None),
    ]
    non_reciprocal_followers_count: Annotated[
        int | None,
        Field(default=None),
    ]
    secret_fans: Annotated[
        int | None,
        Field(default=None),
    ]
    created_at: Annotated[
        date | None,
        Field(default_factory=lambda: now().date()),
    ]


class InstagramUserStatistics(ISchema):
    user_id: Annotated[
        int,
        Field(...),
    ]
    likes_count: Annotated[
        int,
        Field(...),
    ]
    comments_count: Annotated[
        int,
        Field(...),
    ]
    followers_count: Annotated[
        int,
        Field(...),
    ]
    following_count: Annotated[
        int,
        Field(...),
    ]
    mutual_subscriptions_count: Annotated[
        int,
        Field(...),
    ]
    non_reciprocal_following_count: Annotated[
        int,
        Field(...),
    ]
    non_reciprocal_followers_count: Annotated[
        int,
        Field(...),
    ]
    created_at: Annotated[
        date,
        Field(default_factory=lambda: now().date()),
    ]

    @classmethod
    def from_instaloader_profile(
        cls,
        profile: Profile,
        user_id: int,
        mutual_count: int = 0,
        not_following_back_count: int = 0,
        not_followed_by_count: int = 0,
        max_posts: int = 10,
    ) -> "InstagramUserStatistics":
        posts = profile.get_posts()
        likes_count = 0
        comments_count = 0

        for i, post in enumerate(posts):
            if i >= max_posts:
                break
            likes_count += post.likes
            comments_count += post.comments
            sleep(uniform(0.4, 0.9))  # антибан

        return cls(
            user_id=user_id,
            likes_count=likes_count,
            comments_count=comments_count,
            followers_count=profile.followers,
            following_count=profile.followees,
            mutual_subscriptions_count=mutual_count,
            non_reciprocal_following_count=not_followed_by_count,
            non_reciprocal_followers_count=not_following_back_count,
        )


class IInstagramPost(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
    post_url: Annotated[
        str,
        Field(...),
    ]
    thumbnail_url: Annotated[
        str | None,
        Field(default=None),
    ]
    likes_count: Annotated[
        int,
        Field(...),
    ]
    comments_count: Annotated[
        int,
        Field(...),
    ]
    views_count: Annotated[
        int | None,
        Field(default=0),
    ]
    avg_likes: Annotated[
        float,
        Field(default=0),
    ]
    avg_views: Annotated[
        float,
        Field(default=0),
    ]


class InstagramPost(ISchema):
    user_id: Annotated[
        int,
        Field(...),
    ]
    likes_count: Annotated[
        int,
        Field(...),
    ]
    comments_count: Annotated[
        int,
        Field(...),
    ]
    views_count: Annotated[
        int | None,
        Field(default=0),
    ]
    avg_likes: Annotated[
        float,
        Field(default=0),
    ]
    avg_views: Annotated[
        float,
        Field(default=0),
    ]
    post_url: Annotated[
        str,
        Field(...),
    ]
    thumbnail_url: Annotated[
        str | None,
        Field(default=None),
    ]

    @classmethod
    def from_instaloader_post(
        cls,
        post: Post,
        user_id: int,
    ) -> "InstagramPost":
        return cls(
            user_id=user_id,
            likes_count=post.likes,
            comments_count=post.comments,
            views_count=getattr(post, "video_view_count", 0),
            post_url=f"https://www.instagram.com/p/{post.shortcode}/",
            thumbnail_url=post.url,
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
    profile_picture: Annotated[
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
    is_business_account: Annotated[
        bool,
        Field(...),
    ]


class InstagramUserResponse(InstagramUser):
    statistics: Annotated[
        list[IInstagramUserStatistics],
        Field(...),
    ]
    posts: Annotated[
        list[IInstagramPost],
        Field(...),
    ]


class InstagramFollower(ISchema):
    user_id: Annotated[
        int,
        Field(...),
    ]
    relation_type: Literal[
        "follower",
        "following",
        "not_following_back",
        "not_followed_by",
        "secret_fan",
        "unfollower",
        "mutual",
    ]
    related_user_id: Annotated[
        str | None,
        Field(default=None),
    ]
    related_username: Annotated[
        str,
        Field(...),
    ]
    related_full_name: Annotated[
        str | None,
        Field(default=None),
    ]
    profile_picture: Annotated[
        HttpUrl,
        Field(...),
    ]
    created_at: Annotated[
        datetime,
        Field(default_factory=lambda: now()),
    ]

    @classmethod
    def from_instaloader_profile(
        cls,
        user: UserShort,
        user_id: int,
        relation_type: str,
    ) -> "InstagramFollower":
        return cls(
            user_id=user_id,
            relation_type=relation_type,
            related_user_id=str(user.pk),  # pk = Instagram internal ID
            related_username=user.username,
            related_full_name=user.full_name or None,
            profile_picture=user.profile_pic_url,
        )


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
        value: str | Any,
    ) -> Any:
        if isinstance(value, str):
            value = value.strip()
            if value.startswith("```json"):
                value = value.removeprefix("```json").strip()
            if value.endswith("```"):
                value = value.removesuffix("```").strip()
            return loads(value)
        return value


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
    error: Annotated[
        Any | None,
        Field(default=None),
    ]

    def fetch_data(
        self,
    ) -> list[ChatGPTCosmetic]:
        return self.choices[0].message.content


class ChatGPTInstagram(ISchema):
    description: Annotated[
        str,
        Field(...),
    ]
    hashtags: Annotated[
        list[str],
        Field(...),
    ]


class ChatGPTInstagramMessage(ISchema):
    content: Annotated[
        ChatGPTInstagram,
        Field(...),
    ]

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(
        cls,
        value,
    ) -> Any:
        return loads(value)


class ChatGPTInstagramChoice(ISchema):
    index: Annotated[
        int,
        Field(...),
    ]
    message: Annotated[
        ChatGPTInstagramMessage,
        Field(...),
    ]


class ChatGPTInstagramResponse(ISchema):
    choices: Annotated[
        list[ChatGPTInstagramChoice],
        Field(...),
    ]

    def fetch_data(
        self,
    ) -> ChatGPTInstagram:
        return self.choices[0].message.content


class TopmediaAuthData(ISchema):
    member_id: Annotated[
        str,
        Field(...),
    ]
    member_code: Annotated[
        str,
        Field(...),
    ]
    access_token: Annotated[
        str,
        Field(..., alias="token"),
    ]
    email: Annotated[
        str,
        Field(...),
    ]


class TopmediaTokenData(ISchema):
    can_use_pro: Annotated[
        int,
        Field(...),
    ]
    gen_pro_times: Annotated[
        int,
        Field(...),
    ]
    pro_times: Annotated[
        int,
        Field(...),
    ]


class TopmediaSlangData(ISchema):
    accent: Annotated[
        str,
        Field(...),
    ]
    accent_flag: Annotated[
        str,
        Field(...),
    ]
    accent_flag_png: Annotated[
        str,
        Field(...),
    ]
    recognized: Annotated[
        list[str | Any],
        Field(...),
    ]
    show_accent: Annotated[
        list[str | Any],
        Field(...),
    ]


class TopmediaSpeechData(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
    audition_status: Annotated[
        int,
        Field(...),
    ]
    oss_url: Annotated[
        str,
        Field(...),
    ]
    oss_path: Annotated[
        str,
        Field(...),
    ]
    name: Annotated[
        str,
        Field(..., alias="display_name"),
    ]


class TopmediaOssData(ISchema):
    url: Annotated[
        str,
        Field(...),
    ]


class TopmediaSpeechResponse(ISchema):
    type: Annotated[
        int,
        Field(default=0),
    ]
    name: Annotated[
        str,
        Field(...),
    ]
    speaker: Annotated[
        str,
        Field(...),
    ]
    oss_url: Annotated[
        str,
        Field(...),
    ]


class TopmediaSongResponse(ISchema):
    type: Annotated[
        int,
        Field(default=0),
    ]
    title: Annotated[
        str,
        Field(...),
    ]
    song_url: Annotated[
        str,
        Field(...),
    ]

    @model_validator(mode="after")
    def format_song_url(
        self,
    ) -> "TopmediaSongResponse":
        if self.song_url.endswith(".mp3"):
            return self

        if not self.song_url.startswith("http"):
            self.song_url = f"https://files.topmediai.com/aimusic/web/{self.song_url}/{self.title}.mp3"
        else:
            self.song_url = f"{self.song_url}/{self.title}.mp3"
        return self


class TopmediaSongData(ISchema):
    song_ids: Annotated[
        list[str],
        Field(...),
    ]


class TopmediaMusicData(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
    song_id: Annotated[
        str | None,
        Field(default=None),
    ]
    title: Annotated[
        str | None,
        Field(default=None),
    ]
    is_upload: Annotated[
        int,
        Field(...),
    ]
    create_time: Annotated[
        str,
        Field(...),
    ]


class TopmediaMusicResponse(ISchema):
    result: Annotated[
        list[TopmediaMusicData],
        Field(...),
    ]


class TopmediaResponse(ISchema):
    code: Annotated[
        int | None,
        Field(default=None),
    ]
    status: Annotated[
        int | None,
        Field(default=None),
    ]
    resp: Annotated[
        TopmediaAuthData
        | TopmediaTokenData
        | TopmediaSlangData
        | TopmediaSpeechData
        | TopmediaOssData
        | TopmediaSpeechResponse
        | TopmediaSongData
        | TopmediaSongResponse
        | TopmediaMusicResponse,
        Field(..., alias="data"),
    ]
    msg: Annotated[
        str,
        Field(default="Success", alias="message"),
    ]


class TopmediaAPIResponseData(ISchema):
    status: Annotated[
        int,
        Field(...),
    ]
    message: Annotated[
        str,
        Field(default="Success"),
    ]
    data: Annotated[
        TopmediaSpeechResponse | list[TopmediaSongResponse],
        Field(...),
    ]


class TopmediaAPIResponse(ISchema):
    message: Annotated[
        str,
        Field(default="Speech"),
    ]
    resp: Annotated[
        TopmediaAPIResponseData,
        Field(..., alias="data"),
    ]


class ChartData(ISchema):
    month: Annotated[
        str,
        Field(...),
    ]
    count: Annotated[
        int,
        Field(...),
    ]
