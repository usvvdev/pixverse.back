# coding utf-8

from .pixverse import pixverse_router

from .account import account_router

from .auth_user import auth_user_router

from .style import style_router

from .template import template_router

from .application import application_router

__all__: list[str] = [
    "pixverse_router",
    "account_router",
    "auth_user_router",
    "style_router",
    "template_router",
    "application_router",
]
