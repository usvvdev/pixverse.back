# coding utf-8

from fastapi import UploadFile

from fastapi.security import OAuth2PasswordRequestForm

from asyncio import sleep

from .core import PixVerseCore

from .webdriver import PixVerseDriver

from ....interface.schemas.api import (
    StatusBody,
    ResponseModel,
    UserCredentials,
)

from ....domain.tools import save_temp_file

from ....domain.conf import app_conf

from ....domain.entities import (
    IBody,
    APIHeaders,
    IConfEnv,
)

from ....domain.entities.typing.enums import PixVerseUri


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
        body: OAuth2PasswordRequestForm,
    ) -> ResponseModel:
        return await self._core.post(
            endpoint=PixVerseUri.AUTH,
            body=UserCredentials(
                **body.__dict__,
            ),
        )

    async def text_to_video(
        self,
        token: str,
        body: IBody,
    ) -> ResponseModel:
        driver = PixVerseDriver(
            token=token,
        )
        driver.open_web()

        await sleep(2)
        driver.enter_prompt(body.prompt)
        driver.create_generation()
        await sleep(2)

        try:
            return driver.get_logs(PixVerseUri.TEXT)
        finally:
            driver.quit()

    async def image_to_video(
        self,
        token: str,
        body: IBody,
        file: UploadFile,
    ) -> ResponseModel:
        tmp_path: str = save_temp_file(
            file,
        )
        driver = PixVerseDriver(
            token=token,
        )
        driver.open_web()
        await sleep(2)

        driver.upload_image(tmp_path)
        await sleep(2)
        driver.enter_prompt(body.prompt)
        await sleep(2)
        driver.create_generation()
        await sleep(2)

        try:
            return driver.get_logs(PixVerseUri.IMAGE)
        finally:
            driver.quit()

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
