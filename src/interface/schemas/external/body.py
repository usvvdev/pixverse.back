# coding utf-8

from typing import Annotated

from pydantic import Field, field_validator

from ....domain.entities.core import ISchema

from ....domain.entities.pixverse import IBody

from ....domain.constants import PIXVERSE_MEDIA_URL


class UploadIMG(ISchema):
    name: Annotated[
        str,
        Field(...),
    ]
    size: Annotated[
        int,
        Field(...),
    ]
    path: Annotated[
        str,
        Field(...),
    ]


class T2VBody(IBody):
    aspect_ratio: Annotated[
        str,
        Field(default="16:9"),
    ]


class V2VBody(ISchema):
    restyle_id: Annotated[
        int,
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
        str,
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


class I2VBody(IBody):
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


class IMGBody(ISchema):
    images: list[UploadIMG]


class Filter(ISchema):
    off_peak: Annotated[
        int,
        Field(default=0),
    ]


class StatusBody(ISchema):
    offset: Annotated[
        int,
        Field(default=0),
    ]
    limit: Annotated[
        int,
        Field(default=50),
    ]
    filter: Annotated[
        Filter,
        Field(default=Filter()),
    ]
    web_offset: Annotated[
        int,
        Field(default=0),
    ]
    app_offset: Annotated[
        int,
        Field(default=0),
    ]


class GenBody(ISchema):
    video_id: Annotated[
        int,
        Field(...),
    ]


class TemplateBody(ISchema):
    offset: Annotated[
        int,
        Field(default=0),
    ]
    limit: Annotated[
        int,
        Field(default=100),
    ]
