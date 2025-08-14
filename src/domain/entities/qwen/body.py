# coding utf-8

from fastapi import UploadFile

from typing import Annotated, Any

from pendulum import now

from uuid import uuid4

from hashlib import sha256

from pydantic import (
    Field,
    field_validator,
)

from ..core import ISchema

from ...constants import MEDIA_SIZES


class IQwenAccount(ISchema):
    usage_count: Annotated[
        int,
        Field(...),
    ]

    @field_validator("usage_count", mode="after")
    @classmethod
    def validate_usage_count(
        cls,
        value: int,
    ) -> int:
        return value + 1


class QwenLoginBody(ISchema):
    email: Annotated[
        str,
        Field(...),
    ]
    password: Annotated[
        str,
        Field(...),
    ]

    @field_validator("password", mode="after")
    @classmethod
    def validate_password(
        cls,
        value: str,
    ) -> str:
        return sha256(value.encode()).hexdigest()


class IQwenChat(ISchema):
    chat_mode: Annotated[
        str,
        Field(default="normal"),
    ]
    chat_type: Annotated[
        str,
        Field(default="t2i"),
    ]
    models: Annotated[
        list[str],
        Field(default=["qwen3-235b-a22b"]),
    ]
    timestamp: Annotated[
        int,
        Field(default_factory=lambda: now().int_timestamp),
    ]
    title: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4())),
    ]


class IFeatureConfig(ISchema):
    thinking_enabled: Annotated[
        bool,
        Field(default=False),
    ]
    output_schema: Annotated[
        str,
        Field(default="phase"),
    ]


class IQwenChatMessage(ISchema):
    fid: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4())),
    ]
    parent_id: Annotated[
        str | None,
        Field(default=None, alias="parentId"),
    ]
    children_ids: Annotated[
        list[str],
        Field(..., alias="childrenIds"),
    ]
    role: Annotated[
        str,
        Field(default="user"),
    ]
    content: Annotated[
        str,
        Field(...),
    ]
    user_action: Annotated[
        str,
        Field(default="chat"),
    ]
    files: Annotated[
        list[str],
        Field(default=[]),
    ]
    timestamp: Annotated[
        int,
        Field(default_factory=lambda: now().int_timestamp),
    ]
    models: Annotated[
        list[str],
        Field(default=["qwen3-235b-a22b"]),
    ]
    chat_type: Annotated[
        str,
        Field(default="t2i"),
    ]
    feature_config: Annotated[
        IFeatureConfig,
        Field(default=IFeatureConfig()),
    ]
    extra: Annotated[
        dict[str, dict[str, str]],
        Field(default={"meta": {"subChatType": "t2i"}}),
    ]
    sub_chat_type: Annotated[
        str,
        Field(default="t2i"),
    ]
    parent_id: Annotated[
        str | None,
        Field(default=None),
    ]


class IQwenPhotoBody(ISchema):
    stream: Annotated[
        bool,
        Field(default=False),
    ]
    incremental_output: Annotated[
        bool,
        Field(default=True),
    ]
    chat_id: Annotated[
        str,
        Field(...),
    ]
    chat_mode: Annotated[
        str,
        Field(default="normal"),
    ]
    model: Annotated[
        str,
        Field(default="qwen3-235b-a22b"),
    ]
    parent_id: Annotated[
        str | None,
        Field(default=None),
    ]
    messages: Annotated[
        list[IQwenChatMessage],
        Field(...),
    ]
    timestamp: Annotated[
        int,
        Field(default_factory=lambda: now().int_timestamp),
    ]
    size: Annotated[
        str,
        Field(...),
    ]


class IT2IBody(ISchema):
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]
    media_size: Annotated[
        MEDIA_SIZES,
        Field(default="16:9", alias="mediaSize"),
    ]


class IPhotoBody(ISchema):
    filename: Annotated[
        str,
        Field(default_factory=lambda: f"{str(uuid4())}.jpg"),
    ]
    filesize: Annotated[
        int,
        Field(...),
    ]
    filetype: Annotated[
        str,
        Field(default="image"),
    ]
