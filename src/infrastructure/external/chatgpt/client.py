# coding utf-8

from fastapi import UploadFile

from .core import ChatGPTCore

from ....domain.conf import app_conf

from ....domain.entities.core import IConfEnv

from ...orm.database.repositories import PixverseTemplateRepository

from ....domain.repositories import IDatabase

from ....domain.tools import (
    upload_chatgpt_file,
    b64_json_to_image,
)

from ....domain.entities.chatgpt import (
    IBody,
    T2PBody,
    PhotoBody,
)

from ....domain.typing.enums import ChatGPTEndpoint

from ....interface.schemas.api import Template

from ....interface.schemas.external import (
    ChatGPTResponse,
    ChatGPTResp,
)


conf: IConfEnv = app_conf()


templates_database = PixverseTemplateRepository(
    engine=IDatabase(conf),
)


class ChatGPTClient:
    """Клиентский интерфейс для работы с ChatGPT API.

    Предоставляет удобные методы для основных операций с видео контентом:
    - Генерация видео из текста
    - Создание видео из изображений
    - Проверка статуса задач

    Args:
        core (ChatGPTCore): Базовый клиент для выполнения запросов
    """

    def __init__(
        self,
        core: ChatGPTCore,
    ) -> None:
        self._core = core

    async def text_to_photo(
        self,
        body: IBody,
    ) -> ChatGPTResp:
        response: ChatGPTResponse = await self._core.post(
            endpoint=ChatGPTEndpoint.TEXT,
            body=PhotoBody(prompt=body.prompt),
        )
        return ChatGPTResp(
            url=b64_json_to_image(response.data[0].b64_json),
        )

    async def photo_to_photo(
        self,
        body: IBody,
        image: UploadFile,
    ):
        files = await upload_chatgpt_file(
            body,
            image,
        )
        response: ChatGPTResponse = await self._core.post(
            endpoint=ChatGPTEndpoint.PHOTO,
            files=files,
        )
        return ChatGPTResp(
            url=b64_json_to_image(response.data[0].b64_json),
        )

    async def template_to_photo(
        self,
        body: T2PBody,
        image: UploadFile,
    ) -> ChatGPTResp:
        template: Template | None = await templates_database.fetch_template(
            "template_id",
            body.template_id,
        )
        files = await upload_chatgpt_file(
            template,
            image,
        )
        response: ChatGPTResponse = await self._core.post(
            endpoint=ChatGPTEndpoint.PHOTO,
            files=files,
        )
        return ChatGPTResp(
            url=b64_json_to_image(response.data[0].b64_json),
        )
