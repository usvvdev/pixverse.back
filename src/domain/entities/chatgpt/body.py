# coding utf-8

from typing import Annotated

from pydantic import Field

from ..core import ISchema


class IBody(ISchema):
    """Базовое тело запроса для конфигурации AI-модели.

    Содержит обязательные параметры для работы с AI-моделью:
    - Выбор конкретной модели
    - Длительность обработки
    - Текст запроса (промпт)
    - Качество результата

    Наследует все особенности сериализации от ISchema.
    """

    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    prompt: Annotated[
        str,
        Field(...),
    ]


class PhotoBody(ISchema):
    prompt: Annotated[
        str,
        Field(...),
    ]
    model: Annotated[
        str,
        Field(default="gpt-image-1"),
    ]
    size: Annotated[
        str,
        Field(default="auto"),
    ]


class T2PBody(ISchema):
    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    id: Annotated[
        int,
        Field(...),
    ]


class TB2PBody(ISchema):
    user_id: Annotated[
        str,
        Field(..., alias="userId"),
    ]
    app_id: Annotated[
        str,
        Field(..., alias="appId"),
    ]
    box_name: Annotated[
        str,
        Field(..., alias="boxName"),
    ]
    id: Annotated[
        int | None,
        Field(default=None),
    ]
    box_color: Annotated[
        str | None,
        Field(default=None, alias="boxColor"),
    ]
    in_box: Annotated[
        str | None,
        Field(default=None, alias="inBox"),
    ]
