# coding utf-8

from typing import Annotated

from uuid import uuid4

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


class IPixverseBody(ISchema):
    user_id: Annotated[
        str,
        Field(..., alias="userId"),
    ]
    app_id: Annotated[
        str,
        Field(..., alias="appId"),
    ]


class T2VBody(IPixverseBody):
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]


class I2VBody(IPixverseBody):
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]


class R2VBody(IPixverseBody):
    template_id: Annotated[
        str | None,
        Field(default=None, alias="templateId"),
    ]


class TE2VBody(IPixverseBody):
    template_id: Annotated[
        str | None,
        Field(default=None, alias="templateId"),
    ]


class IMGBody(ISchema):
    images: list[UploadIMG]


class VideoBody(ISchema):
    name: Annotated[
        str,
        Field(...),
    ]
    path: Annotated[
        str,
        Field(...),
    ]
    type: Annotated[
        int,
        Field(default=1),
    ]

    @field_validator("path", mode="after")
    @classmethod
    def validate_image_path(
        cls,
        value: str,
    ) -> str:
        return "".join(("upload/", value))


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


class GenerationData(ISchema):
    uuid: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4())),
    ]
    generation_id: Annotated[
        int,
        Field(...),
    ]
    account_id: Annotated[
        int,
        Field(...),
    ]
    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]


class UsrData(ISchema):
    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    app_id_usage: Annotated[
        int,
        Field(default=1),
    ]


class UserToken(ISchema):
    account_id: Annotated[
        int,
        Field(...),
    ]
    jwt_token: Annotated[
        str,
        Field(...),
    ]
