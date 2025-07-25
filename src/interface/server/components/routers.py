# coding utf-8

from fastapi import FastAPI

from ..routing import AppRouting

from ....domain.entities.core import IConfEnv

from ....infrastructure.api.routes.v1 import (
    pixverse_router,
    pixverse_account_router,
    auth_user_router,
    pixverse_style_router,
    pixverse_template_router,
    pixverse_application_router,
    chatgpt_router,
    photo_generator_template_router,
    photo_generator_application_router,
    user_data_router,
    calories_router,
    application_router,
    media_router,
    instagram_router,
    webhook_router,
    product_router,
)


class PixVerseRouter(AppRouting):
    def __init__(
        self,
        app: FastAPI,
        config: IConfEnv,
    ) -> None:
        """Специализированный роутер для API PixVerse.

        Наследует базовый функционал регистрации роутеров и добавляет
        предварительно настроенный роутер PixVerse API.

        Args:
            app (FastAPI): Экземпляр FastAPI приложения
            config (IConfEnv): Конфигурация приложения
        """
        super().__init__(
            app,
            config,
            routers=[
                pixverse_router,
                pixverse_style_router,
                pixverse_template_router,
                pixverse_application_router,
                media_router,
                webhook_router,
            ],
        )


class ChatGPTRouter(AppRouting):
    def __init__(
        self,
        app: FastAPI,
        config: IConfEnv,
    ) -> None:
        """Специализированный роутер для API PixVerse.

        Наследует базовый функционал регистрации роутеров и добавляет
        предварительно настроенный роутер PixVerse API.

        Args:
            app (FastAPI): Экземпляр FastAPI приложения
            config (IConfEnv): Конфигурация приложения
        """
        super().__init__(
            app,
            config,
            routers=[
                chatgpt_router,
                photo_generator_template_router,
                photo_generator_application_router,
                media_router,
            ],
        )


class AuthRouter(AppRouting):
    def __init__(
        self,
        app: FastAPI,
        config: IConfEnv,
    ) -> None:
        super().__init__(
            app,
            config,
            routers=[
                auth_user_router,
            ],
        )


class DashboardRouter(AppRouting):
    def __init__(
        self,
        app: FastAPI,
        config: IConfEnv,
    ) -> None:
        super().__init__(
            app,
            config,
            routers=[
                pixverse_account_router,
                pixverse_style_router,
                pixverse_template_router,
                pixverse_application_router,
                user_data_router,
                application_router,
                media_router,
                product_router,
            ],
        )


class CaloriesRouter(AppRouting):
    def __init__(
        self,
        app: FastAPI,
        config: IConfEnv,
    ) -> None:
        super().__init__(
            app,
            config,
            routers=[
                calories_router,
                media_router,
            ],
        )


class InstagramRouter(AppRouting):
    def __init__(
        self,
        app: FastAPI,
        config: IConfEnv,
    ) -> None:
        super().__init__(
            app,
            config,
            routers=[
                instagram_router,
                media_router,
            ],
        )
