# coding utf-8

from .core import PixVerseCore

from .webdriver import PixVerseDriver

from ....interface.schemas.api import (
    StatusBody,
    ResponseModel,
    UserCredentials,
)

from ....domain.entities import IBody

from ....domain.entities.typing.enums import PixVerseUri

from ....domain.entities import (
    APIHeaders,
    IConfEnv,
)

from ....domain.conf import app_conf

from asyncio import sleep


conf: IConfEnv = app_conf()


class PixVerseClient:
    """Клиентский интерфейс для работы с PixVerse API.

    Предоставляет удобные методы для основных операций с видео контентом:
    - Генерация видео из текста
    - Создание видео из изображений
    - Проверка статуса задач

    Args:
        core (PixVerseCore): Базовый клиент для выполнения запросов
    """

    def __init__(
        self,
        core: PixVerseCore,
    ) -> None:
        self._core = core

    async def auth_user(
        self,
        body: UserCredentials,
    ) -> ResponseModel:
        return await self._core.post(
            endpoint=PixVerseUri.AUTH,
            body=body,
        )

    async def text_to_video(
        self,
        token: str,
        body: IBody,
    ) -> ResponseModel:
        driver = PixVerseDriver(token=token)
        driver.open_web()

        await sleep(2)
        driver.enter_prompt(body.prompt)

        driver.create_generation()
        await sleep(2)

        logs = driver.get_logs(PixVerseUri.TEXT)

        driver.quit()
        return logs

    async def image_to_video(
        self,
        body: IBody,
        token: str,
        file: str,
    ) -> ResponseModel:
        driver = PixVerseDriver(token=token)
        driver.open_web()
        await sleep(2)

        driver.upload_image(str(file))

        await sleep(2)
        driver.enter_prompt(body.prompt)

        await sleep(2)
        driver.create_generation()

        await sleep(2)
        logs = driver.get_logs(PixVerseUri.IMAGE)

        driver.quit()
        return logs

    async def generation_status(
        self,
        body: StatusBody,
    ) -> ResponseModel:
        return await self._core.get(
            endpoint=PixVerseUri.STATUS.format(
                id=body.generation_id,
            ),
            headers=APIHeaders(
                api_key=conf.api_key,
            ).dict,
        )
