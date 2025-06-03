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


class RVBody(IPixverseBody):
    template_id: Annotated[
        str,
        Field(..., alias="templateId"),
    ]


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
