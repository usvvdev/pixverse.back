# coding utf-8

from .pixverse import (
    PixVerseViewFactory,
    PixverseTemplateViewFactory,
    PixverseAccountViewFactory,
    PixverseStyleViewFactory,
    PixverseApplicationViewFactory,
    UserDataViewFactory,
)

from .auth import AuthUserViewFactory

from .chatgpt import (
    ChatGPTViewFactory,
    PhotoGeneratorApplicationViewFactory,
    PhotoGeneratorTemplateViewFactory,
)

from .calories import CaloriesViewFactory

from .common import ApplicationViewFactory

from .instagram import InstagramViewFactory

__all__: list[str] = [
    "PixVerseViewFactory",
    "PixverseAccountViewFactory",
    "AuthUserViewFactory",
    "PixverseStyleViewFactory",
    "PixverseTemplateViewFactory",
    "PixverseApplicationViewFactory",
    "UserDataViewFactory",
    "ChatGPTViewFactory",
    "PhotoGeneratorApplicationViewFactory",
    "PhotoGeneratorTemplateViewFactory",
    "CaloriesViewFactory",
    "ApplicationViewFactory",
    "InstagramViewFactory",
]
