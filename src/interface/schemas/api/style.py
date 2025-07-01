# coding utf-8

from typing import Annotated

from pydantic import (
    Field,
    field_validator,
)

from ....domain.conf import app_conf

from ....domain.entities.core import (
    ISchema,
    IConfEnv,
)

from ....infrastructure.orm.database.models import PixverseStyles


conf: IConfEnv = app_conf()


class IStyle(ISchema):
    prompt: Annotated[
        str,
        Field(...),
    ]
    name: Annotated[
        str,
        Field(...),
    ]
    is_active: Annotated[
        bool,
        Field(default=True),
    ]

    @field_validator("name", mode="before")
    @classmethod
    def validate_app_id(
        cls,
        value: str,
    ) -> str:
        return " ".join(value.split())


class ChangeStyle(IStyle):
    preview_small: Annotated[
        str | None,
        Field(default=None),
    ]
    preview_large: Annotated[
        str | None,
        Field(default=None),
    ]


class Style(ChangeStyle):
    id: Annotated[
        int,
        Field(...),
    ]
    template_id: Annotated[
        int | None,
        Field(default=None),
    ]

    @field_validator("preview_small", mode="after")
    @classmethod
    def create_preview_small_url(
        cls,
        value: str,
    ) -> str:
        return (
            "".join((conf.domain_url, value.replace("uploads/", "/static/")))
            if value is not None
            else value
        )

    @field_validator("preview_large", mode="after")
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

    @classmethod
    def create(
        cls,
        styles: list[PixverseStyles],
    ) -> list["Style"]:
        return list(
            map(
                lambda style: cls.model_validate(style),
                styles,
            ),
        )
