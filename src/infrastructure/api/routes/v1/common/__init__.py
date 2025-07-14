# coding utf-8

from .application import application_router

from .media import media_router

__all__: list[str] = [
    "application_router",
    "media_router",
]
