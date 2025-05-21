# coding utf-8

from typing import Any

from ..web3 import Web3

from ....domain.constants import PIXVERSE_BASE_URL

from ....domain.entities.typing.enums import RequestMethod


class PixVerseCore(Web3):
    """Базовый клиент для работы с PixVerse API.

    Наследует функциональность Web3 клиента и добавляет специализированные методы
    для взаимодействия с PixVerse API. Автоматически использует базовый URL сервиса.

    Args:
        headers (dict[str, Any]): Заголовки HTTP-запросов (должен содержать API-ключ)
    """

    def __init__(
        self,
        headers: dict[str, Any],
    ) -> None:
        """Инициализация клиента PixVerse.

        Args:
            headers (dict): Заголовки запросов, обязательно включающие:
                - 'API-KEY': Ключ авторизации
        """
        super().__init__(
            PIXVERSE_BASE_URL,  # Базовый URL из конфигурации
            headers,
        )

    async def post(
        self,
        *args,
        **kwargs,
    ) -> dict[str, Any]:
        """Отправка POST-запроса к PixVerse API.

        Args:
            *args: Позиционные аргументы для send_request:
                - endpoint (str): Конечная точка API
                - body (ISchema, optional): Тело запроса
            **kwargs: Именованные аргументы для send_request

        Returns:
            dict[str, Any]: Ответ API в формате JSON

        """
        return await super().send_request(
            RequestMethod.POST,
            *args,
            **kwargs,
        )

    async def get(
        self,
        *args,
        **kwargs,
    ) -> dict[str, Any]:
        """Отправка GET-запроса к PixVerse API.

        Args:
            *args: Позиционные аргументы для send_request:
                - endpoint (str): Конечная точка API
            **kwargs: Именованные аргументы для send_request

        Returns:
            dict[str, Any]: Ответ API в формате JSON

        """
        return await super().send_request(
            RequestMethod.GET,
            *args,
            **kwargs,
        )
