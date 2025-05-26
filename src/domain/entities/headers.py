# coding utf-8

from typing import Annotated

from pydantic import Field

from uuid import uuid4

from .base import ISchema


class IHeaders(ISchema):
    """Базовые HTTP-заголовки для запросов к AI API.

    Содержит обязательные и опциональные заголовки для взаимодействия
    с API искусственного интеллекта. Наследует функциональность
    сериализации от ISchema.

    Особенности:
    - Автоматическая генерация trace_id при отсутствии
    - Использование стандартных алиасов для заголовков
    """

    trace_id: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4()), alias="Ai-trace-id"),
    ]
    """Уникальный идентификатор цепочки запросов (trace ID).
    
    Тип:
        str (UUID в строковом формате)
    Значение по умолчанию:
        Автоматически генерируется при создании (uuid4)
    Алиас в заголовке:
        Ai-trace-id
    Назначение:
        Для сквозной трассировки запросов в распределенных системах
    """


class TokenHeaders(IHeaders):
    token: Annotated[
        str,
        Field(..., alias="Token"),
    ]
    """ Ключ аутентификации (JWT) для API.
    
    Тип:
        str
    Обязательное поле:
        Да
    Алиас в заголовке:
        Token
    """


class APIHeaders(IHeaders):
    api_key: Annotated[
        str,
        Field(..., alias="API-KEY"),
    ]
    """ Секретный ключ для API.
    
    Тип:
        str
    Обязательное поле:
        Да
    Алиас в заголовке:
        API-KEY
    """
