# coding utf-8

from typing import Annotated

from pydantic import Field

from ..core import ISchema

from ...typing import (
    TModel,
    TQuality,
)


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
    """Текст запроса (промпт) для обработки AI-моделью.
    
    Тип:
        str: Непустая строка
    Обязательное поле.
    """

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
