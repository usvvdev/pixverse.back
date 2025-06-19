# coding utf-8

from .pixverse import (
    pixverse_router,
    pixverse_account_router,
    pixverse_style_router,
    pixverse_template_router,
    pixverse_application_router,
    user_data_router,
)

from .auth import auth_user_router

from .chatgpt import (
    chatgpt_router,
    photo_generator_application_router,
    photo_generator_template_router,
)

__all__: list[str] = [
    "auth_user_router",
    "pixverse_router",
    "pixverse_account_router",
    "pixverse_style_router",
    "pixverse_template_router",
    "pixverse_application_router",
    "user_data_router",
    "chatgpt_router",
    "photo_generator_application_router",
    "photo_generator_template_router",
]
