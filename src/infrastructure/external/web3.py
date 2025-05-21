# coding utf-8

from typing import (
    AsyncGenerator,
    Any,
)

from httpx import (
    AsyncClient,
    Response,
)

from ...domain.entities import ISchema


class Web3:
    """Клиент для взаимодействия с Web3 API.

    Обеспечивает асинхронное подключение и выполнение запросов к Web3 сервисам.
    Поддерживает повторное использование соединений и автоматическое управление ресурсами.

    Args:
        url (str): Базовый URL API сервиса
        headers (dict[str, Any]): Заголовки для всех запросов (например, авторизация)
    """

    def __init__(
        self,
        url: str,
        headers: dict[str, Any],
    ) -> None:
        """Инициализация Web3 клиента.

        Args:
            url (str): Базовый URL (например, "https://api.web3.service")
            headers (dict): Стандартные заголовки для запросов
        """
        self._url = url
        self._headers = headers

    async def get_client(
        self,
    ) -> AsyncGenerator[AsyncClient, Any]:
        """Асинхронный генератор HTTP клиента с управлением контекстом.

        Yields:
            AsyncClient: Экземпляр асинхронного HTTP клиента

        """
        async with AsyncClient(headers=self._headers) as client:
            yield client

    async def __make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> AsyncGenerator[Response, Any]:
        """Внутренний метод выполнения запроса.

        Args:
            method (str): HTTP метод ("GET", "POST" и т.д.)
            endpoint (str): Конечная точка API
            **kwargs: Дополнительные параметры для запроса

        Yields:
            Response: Объект ответа от сервера

        """
        async for client in self.get_client():
            yield await client.request(
                method,
                url="".join((self._url, endpoint)),
                **kwargs,
            )

    async def send_request(
        self,
        method: str,
        endpoint: str,
        body: ISchema = None,
    ) -> dict[str, Any]:
        """Основной метод отправки запроса к API.

        Args:
            method (str): HTTP метод ("GET", "POST" и т.д.)
            endpoint (str): Относительный путь конечной точки
            body (ISchema, optional): Тело запроса, соответствующее схеме

        Returns:
            dict[str, Any]: Ответ API в виде словаря

        """
        async for response in self.__make_request(
            method,
            endpoint=endpoint,
            json=body.dict if body else None,
        ):
            return response.json()
