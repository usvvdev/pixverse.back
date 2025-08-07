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

from .calories import calories_router

from .common import (
    application_router,
    media_router,
    webhook_router,
    product_router,
)

from .instagram import instagram_router

from .cosmetic import cosmetic_router

from .qwen import qwen_router

from .topmedia import topmedia_router, topmedia_voice_router

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
    "calories_router",
    "application_router",
    "media_router",
    "instagram_router",
    "webhook_router",
    "product_router",
    "cosmetic_router",
    "qwen_router",
    "topmedia_router",
    "topmedia_voice_router",
]
