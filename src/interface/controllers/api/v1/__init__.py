# coding utf-8

from .auth import AuthUserController

from .pixverse import (
    PixverseAccountController,
    PixverseApplicationController,
    PixVerseController,
    PixverseStyleController,
    PixverseTemplateController,
    UserDataController,
)

from .chatgpt import (
    ChatGPTController,
    PhotoGeneratorApplicationController,
    PhotoGeneratorTemplateController,
)

from .calories import CaloriesController

from .common import ApplicationController

__all__: list[str] = [
    "AuthUserController",
    "PixVerseController",
    "PixverseAccountController",
    "PixverseStyleController",
    "PixverseTemplateController",
    "PixverseApplicationController",
    "UserDataController",
    "ChatGPTController",
    "PhotoGeneratorApplicationController",
    "PhotoGeneratorTemplateController",
    "CaloriesController",
    "ApplicationController",
]
