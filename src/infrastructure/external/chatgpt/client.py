# coding utf-8

import os

from fastapi import UploadFile

from asyncio import sleep

from .core import ChatGPTCore

from ....domain.conf import app_conf

from ....domain.errors import (
    PixverseError,
    PhotoGeneratorError,
)

from ....domain.entities.core import IConfEnv

from ...orm.database.repositories import (
    PhotoGeneratorTemplateRepository,
    UserGenerationRepository,
    UserDataRepository,
)

from ...orm.database.models import PhotoGeneratorTemplates

from ....domain.repositories import IDatabase

from ....domain.tools import (
    upload_chatgpt_file,
    b64_json_to_image,
)

from ....domain.entities.chatgpt import (
    IBody,
    T2PBody,
    PhotoBody,
    TB2PBody,
)

from ....domain.typing.enums import ChatGPTEndpoint

from ....interface.schemas.api import Template

from ....interface.schemas.external import (
    ChatGPTResponse,
    ChatGPTResp,
    ChatGPTErrorResponse,
    ChatGPTError,
    GenerationData,
    UsrData,
)

from ....domain.constants import BODY_TOYBOX_PROMT


conf: IConfEnv = app_conf()


templates_database = PhotoGeneratorTemplateRepository(
    engine=IDatabase(conf),
)

user_generations_database = UserGenerationRepository(
    engine=IDatabase(conf),
)

user_data_database = UserDataRepository(
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

    async def __handle_success(
        self,
        user_data: IBody | TB2PBody | T2PBody,
        data: ChatGPTResponse,
    ) -> ChatGPTResp:
        video_data = ChatGPTResp(
            url=b64_json_to_image(data.data[0].b64_json),
        )
        await user_generations_database.add_record(
            GenerationData(
                user_id=user_data.user_id,
                app_id=user_data.app_id,
                app_name=os.getenv("APP_SERVICE").lower(),
                generation_url=video_data.url,
            )
        )
        await user_data_database.create_or_update_user_data(
            UsrData(
                user_id=user_data.user_id,
                app_id=user_data.app_id,
            )
        )
        return video_data

    async def __handle_failure(
        self,
        last_error: ChatGPTError,
        status_code: int | None = None,
        extra: dict[str] = {},
    ) -> PhotoGeneratorError:
        error = PhotoGeneratorError(
            status_code=status_code if status_code is not None else 400,
            detail=last_error.message,
            extra=extra,
        )
        raise error

    async def text_to_photo(
        self,
        body: IBody,
    ) -> ChatGPTResp:
        max_attempts = 10

        last_error = None

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:

                async def call(
                    token: str,
                ) -> ChatGPTResponse | ChatGPTErrorResponse:
                    return await self._core.post(
                        token=token,
                        endpoint=ChatGPTEndpoint.TEXT,
                        body=PhotoBody(
                            prompt=body.prompt,
                        ),
                    )

                data: ChatGPTResponse | ChatGPTErrorResponse = await call(token)

                if not isinstance(data, ChatGPTErrorResponse):
                    return await self.__handle_success(
                        body,
                        data,
                    )

                last_error = data.error

            except Exception:
                if attempt == max_attempts - 1:
                    try:
                        data = await call(token)

                        if not data.error:
                            return await self.__handle_success(
                                body,
                                data,
                            )

                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(last_error)
                await sleep(1)
        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    async def photo_to_photo(
        self,
        body: IBody,
        image: UploadFile,
    ) -> ChatGPTResp:
        max_attempts = 10

        last_error = None

        files = await upload_chatgpt_file(
            body,
            image,
        )

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:

                async def call(
                    token: str,
                ) -> ChatGPTResponse | ChatGPTErrorResponse:
                    return await self._core.post(
                        token=token,
                        endpoint=ChatGPTEndpoint.PHOTO,
                        files=files,
                    )

                data: ChatGPTResponse | ChatGPTErrorResponse = await call(token)

                if not isinstance(data, ChatGPTErrorResponse):
                    return await self.__handle_success(
                        body,
                        data,
                    )

                last_error = data.error

            except Exception:
                if attempt == max_attempts - 1:
                    try:
                        data = await call(token)

                        if not data.error:
                            return await self.__handle_success(
                                body,
                                data,
                            )

                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(last_error)
                await sleep(1)
        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    async def template_to_photo(
        self,
        body: T2PBody,
        image: UploadFile,
    ) -> ChatGPTResp:
        max_attempts = 10

        last_error = None

        template: Template | None = await templates_database.fetch_template(
            "id",
            body.id,
        )
        if template is None:
            raise PixverseError(status_code=500070)

        files = await upload_chatgpt_file(
            template,
            image,
        )

        for attempt in range(max_attempts):
            token = conf.chatgpt_token

            try:

                async def call(
                    token: str,
                ) -> ChatGPTResponse | ChatGPTErrorResponse:
                    return await self._core.post(
                        token=token,
                        endpoint=ChatGPTEndpoint.PHOTO,
                        files=files,
                    )

                data: ChatGPTResponse | ChatGPTErrorResponse = await call(token)

                if not isinstance(data, ChatGPTErrorResponse):
                    return await self.__handle_success(
                        body,
                        data,
                    )

                last_error = data.error

            except Exception:
                if attempt == max_attempts - 1:
                    try:
                        data = await call(token)

                        if not data.error:
                            return await self.__handle_success(
                                body,
                                data,
                            )

                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(last_error)
                await sleep(1)
        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    async def toybox_to_photo(
        self,
        body: TB2PBody,
        image: UploadFile,
    ) -> ChatGPTResp:
        max_attempts = 10

        last_error = None

        data: IBody | PhotoGeneratorTemplates = (
            IBody(
                user_id=body.user_id,
                app_id=body.app_id,
                prompt=BODY_TOYBOX_PROMT.format(
                    box_color=body.box_color,
                    in_box=body.in_box,
                    box_name=body.box_name,
                ),
            )
            if body.box_color and body.in_box is not None
            else await templates_database.fetch_template("id", body.id, body.box_name)
        )

        files = await upload_chatgpt_file(
            data,
            image,
        )

        for attempt in range(max_attempts):
            token = conf.chatgpt_token

            try:

                async def call(
                    token: str,
                ) -> ChatGPTResponse | ChatGPTErrorResponse:
                    return await self._core.post(
                        token=token,
                        endpoint=ChatGPTEndpoint.PHOTO,
                        files=files,
                    )

                data: ChatGPTResponse | ChatGPTErrorResponse = await call(token)

                if not isinstance(data, ChatGPTErrorResponse):
                    return await self.__handle_success(
                        body,
                        data,
                    )

                last_error = data.error

            except Exception:
                if attempt == max_attempts - 1:
                    try:
                        data = await call(token)

                        if not data.error:
                            return await self.__handle_success(
                                body,
                                data,
                            )

                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(last_error)
                await sleep(1)
        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )
