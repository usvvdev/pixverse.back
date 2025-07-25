# coding utf-8

from .pixverse import (
    PixVerseView,
    PixverseTemplateView,
    PixverseAccountView,
    PixverseStyleView,
    PixverseApplicationView,
    UserDataView,
)

from .auth import AuthUserView

from .chatgpt import (
    ChatGPTView,
    PhotoGeneratorTemplateView,
    PhotoGeneratorApplicationView,
)

from .calories import CaloriesView

from .common import (
    ApplicationView,
    ProductView,
)

from .instagram import InstagramView

__all__: list[str] = [
    "PixVerseView",
    "PixverseAccountView",
    "AuthUserView",
    "PixverseStyleView",
    "PixverseTemplateView",
    "PixverseApplicationView",
    "UserDataView",
    "ApplicationView",
    "ChatGPTView",
    "PhotoGeneratorTemplateView",
    "PhotoGeneratorApplicationView",
    "CaloriesView",
    "ApplicationView",
    "InstagramView",
    "ProductView",
]
