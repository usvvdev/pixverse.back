# coding utf-8

from typing import (
    AsyncGenerator,
    Any,
)

from httpx import (
    AsyncClient,
    Response,
)

from ...domain.entities.core import (
    ISchema,
)


class HttpClient:
    """Клиент для взаимодействия с Web3 API.

    Обеспечивает асинхронное подключение и выполнение запросов к Web3 сервисам.
    Поддерживает повторное использование соединений и автоматическое управление ресурсами.

    Args:
        url (str): Базовый URL API сервиса
        headers (dict[str, Any]): Заголовки для всех запросов (например, авторизация)
    """

    def __init__(
        self,
        url: str | dict[str, str],
    ) -> None:
        """Инициализация Web3 клиента.

        Args:
            url (str): Базовый URL (например, "https://api.web3.service")
            headers (dict): Стандартные заголовки для запросов
        """
        self._url = url

    async def get_client(
        self,
        headers: dict[str, Any],
        timeout: int,
    ) -> AsyncGenerator[AsyncClient, Any]:
        """Асинхронный генератор HTTP клиента с управлением контекстом.

        Yields:
            AsyncClient: Экземпляр асинхронного HTTP клиента

        """
        async with AsyncClient(headers=headers, timeout=timeout) as client:
            yield client

    async def __make_request(
        self,
        method: str,
        url_method: str | None,
        endpoint: str,
        headers: dict[str, Any],
        timeout: int,
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
        async for client in self.get_client(headers, timeout):
            api_url: str = (
                self._url.get(url_method) if url_method is not None else self._url
            )
            try:
                yield await client.request(
                    method,
                    url="".join((api_url, endpoint)),
                    **kwargs,
                )
            finally:
                await client.aclose()

    async def send_request(
        self,
        method: str,
        headers: ISchema,
        endpoint: str,
        url_method: str | None = None,
        timeout: int = 60,
        body: ISchema | None = None,
        files=None,
        params: ISchema | None = None,
        data: ISchema | None = None,
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
            url_method,
            endpoint,
            headers.dict if headers else None,
            timeout,
            json=body.dict if body else None,
            files=files if files else None,
            params=params.dict if params else None,
            data=data.dict if data else None,
        ):
            return response.json()
