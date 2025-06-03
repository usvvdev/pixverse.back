# coding utf-8

from typing import Annotated

from pydantic import (
    Field,
    field_validator,
)

from ..core import ISchema

from ...typing import (
    TModel,
    TQuality,
)

from ...constants import PIXVERSE_MEDIA_URL


class IBody(ISchema):
    """Базовое тело запроса для конфигурации AI-модели.

    Содержит обязательные параметры для работы с AI-моделью:
    - Выбор конкретной модели
    - Длительность обработки
    - Текст запроса (промпт)
    - Качество результата

    Наследует все особенности сериализации от ISchema.
    """

    prompt: Annotated[
        str,
        Field(...),
    ]

    duration: Annotated[
        int,
        Field(default=5),
    ]

    quality: Annotated[
        TQuality,
        Field(default="360p"),
    ]

    motion_mode: Annotated[
        str,
        Field(default="normal"),
    ]

    model: Annotated[
        TModel,
        Field(default="v4.5"),
    ]

    lip_sync_tts_speaker_id: Annotated[
        str,
        Field(default="Auto"),
    ]


class IT2VBody(IBody):
    aspect_ratio: Annotated[
        str,
        Field(default="16:9"),
    ]


class LFBody(ISchema):
    video_path: Annotated[
        str,
        Field(...),
    ]
    duration: Annotated[
        int,
        Field(default=5),
    ]


class II2VBody(IBody):
    img_path: Annotated[
        str,
        Field(..., alias="customer_img_path"),
    ]
    img_url: Annotated[
        str,
        Field(..., alias="customer_img_url"),
    ]

    @field_validator("img_path", mode="after")
    @classmethod
    def validate_image_path(
        cls,
        value: str,
    ) -> str:
        return "".join(("upload/", value))

    @field_validator("img_url", mode="after")
    @classmethod
    def validate_image_url(
        cls,
        value: str,
    ) -> str:
        return "".join((PIXVERSE_MEDIA_URL, value))


class IIT2VBody(II2VBody):
    effect_type: Annotated[
        int,
        Field(default=1),
    ]
    sound_effect_switch: Annotated[
        int,
        Field(default=1),
    ]
    template_id: Annotated[
        int,
        Field(...),
    ]


class IRVBody(ISchema):
    restyle_prompt: Annotated[
        str,
        Field(...),
    ]
    model: Annotated[
        str,
        Field(default="v4"),
    ]
    video_url: Annotated[
        str,
        Field(..., alias="customer_video_url"),
    ]
    video_path: Annotated[
        str,
        Field(..., alias="customer_video_path"),
    ]
    video_duration: Annotated[
        int,
        Field(..., alias="customer_video_duration"),
    ]
    last_frame_url: Annotated[
        str,
        Field(..., alias="customer_video_last_frame_url"),
    ]

    @field_validator("video_path", mode="after")
    @classmethod
    def validate_image_path(
        cls,
        value: str,
    ) -> str:
        return "".join(("upload/", value))

    @field_validator("video_url", mode="after")
    @classmethod
    def validate_image_url(
        cls,
        value: str,
    ) -> str:
        return "".join((PIXVERSE_MEDIA_URL, value))
