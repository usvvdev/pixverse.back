# coding utf-8

from typing import Annotated

from pydantic import Field, field_validator

from datetime import datetime

from .template import Template

from .style import Style

from ....domain.entities.core import ISchema


class IApplication(ISchema):
    app_id: Annotated[
        str,
        Field(...),
    ]
    templates: Annotated[
        list[Template] | None,
        Field(default=None),
    ]

    @field_validator("app_id", mode="before")
    @classmethod
    def validate_app_id(
        cls,
        value: str,
    ) -> str:
        return " ".join(value.split())


class PhotoGeneratorApplication(IApplication):
    pass


class PixverseApplication(IApplication):
    styles: Annotated[
        list[Style] | None,
        Field(default=None),
    ]

    @field_validator(
        "styles",
        mode="before",
    )
    @classmethod
    def validate_styles(
        cls,
        value: list,
    ) -> list[Style] | None:
        if len(value) > 0:
            return value
        return None


class ChangeApplication(ISchema):
    app_id: Annotated[
        str,
        Field(...),
    ]
    template_ids: Annotated[
        list[int],
        Field(...),
    ]
    style_ids: Annotated[
        list[int],
        Field(...),
    ]


class Application(PixverseApplication):
    id: Annotated[
        int,
        Field(...),
    ]


class IStoreApplication(ISchema):
    name: Annotated[
        str,
        Field(...),
    ]
    region: Annotated[
        str,
        Field(...),
    ]
    application_number: Annotated[
        int,
        Field(...),
    ]
    technology: Annotated[
        str,
        Field(...),
    ]
    store_region: Annotated[
        str,
        Field(...),
    ]
    application_id: Annotated[
        str,
        Field(...),
    ]
    description: Annotated[
        str,
        Field(...),
    ]
    category: Annotated[
        str,
        Field(...),
    ]


class ChangeStoreApplication(IStoreApplication):
    pass


class AddStoreApplication(IStoreApplication):
    start_date: Annotated[
        datetime,
        Field(...),
    ]
    release_date: Annotated[
        datetime,
        Field(...),
    ]


class StoreApplication(AddStoreApplication):
    id: Annotated[
        int,
        Field(...),
    ]
