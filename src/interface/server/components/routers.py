# coding utf-8

from fastapi import FastAPI

from ..routing import AppRouting

from ....domain.entities import IConfEnv

from ....infrastructure.api.routes.v1 import (
    pixverse_router,
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
            ],
        )
