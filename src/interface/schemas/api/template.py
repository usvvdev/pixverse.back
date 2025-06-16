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

from ....infrastructure.orm.database.models import PixverseTemplates


conf: IConfEnv = app_conf()


class ITemplate(ISchema):
    prompt: Annotated[
        str,
        Field(...),
    ]
    name: Annotated[
        str,
        Field(...),
    ]
    category: Annotated[
        str | None,
        Field(default=None),
    ]
    is_active: Annotated[
        bool,
        Field(default=True),
    ]


class ChangeTemplate(ITemplate):
    preview_small: Annotated[
        str | None,
        Field(default=None),
    ]
    preview_large: Annotated[
        str | None,
        Field(default=None),
    ]
    template_id: Annotated[
        int | None,
        Field(default=None),
    ]


class Template(ChangeTemplate):
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
        templates: list[PixverseTemplates],
    ) -> list["Template"]:
        return list(
            map(
                lambda template: cls.model_validate(template),
                templates,
            ),
        )
