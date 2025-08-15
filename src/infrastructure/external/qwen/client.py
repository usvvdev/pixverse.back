# coding utf-8

from .core import QwenCore

from fastapi import (
    HTTPException,
    UploadFile,
)

from uuid import uuid4

from asyncio import sleep

from ....domain.conf import app_conf

from ....domain.errors import TopmediaError

from ....domain.typing.enums import (
    QwenEndpoint,
    AccountProjectToken,
)

from ....domain.entities.core import (
    IConfEnv,
)

from ....domain.entities.qwen import (
    IT2IBody,
    QwenLoginBody,
    IQwenChat,
    IQwenPhotoBody,
    IQwenChatMessage,
    IPhotoBody,
)

from ...orm.database.models import (
    QwenAccounts,
    QwenAccountsTokens,
)

from ...orm.database.repositories import (
    QwenAccountTokenRepository,
    QwenAccountRepository,
)

from ....domain.repositories import IDatabase

from ....domain.tools import (
    update_account_token,
    upload_qwen_file,
)

from ....interface.schemas.external import (
    QwenResponse,
    QwenAuthResponse,
    QwenErrorResponse,
    QwenMessageContent,
    QwenPhotoAPIResponse,
    QwenUploadData,
)


conf: IConfEnv = app_conf()


account_database = QwenAccountRepository(
    engine=IDatabase(conf),
)


account_token_database = QwenAccountTokenRepository(
    engine=IDatabase(conf),
)


class QwenClient:
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
        core: QwenCore,
    ) -> None:
        self._core = core

    async def auth_user_account(
        self,
        account: QwenAccounts,
    ) -> str:
        data: QwenAuthResponse | QwenErrorResponse = await self._core.post(
            # Request **kwargs
            endpoint=QwenEndpoint.AUTH,
            body=QwenLoginBody(
                email=account.username,
                password=account.password,
            ),
        )

        if not isinstance(data, QwenAuthResponse):
            error = TopmediaError(
                status_code=409,
            )

            raise error
        return data.token

    def __get_media_content(
        self,
        data: QwenResponse,
    ) -> str:
        last_generation_id: str = data.resp.current_id

        if last_generation_id is not None:
            content_list: list[QwenMessageContent] = data.resp.chat.history.messages[
                last_generation_id
            ].content_list

            return content_list[0].content

    async def __handle_failure(
        self,
        status_code: int,
        extra: dict[str] = {},
    ) -> TopmediaError:
        error = TopmediaError(
            status_code=status_code if status_code is not None else 505,
            extra=extra,
        )

        raise error

    async def __fetch_upload_token(
        self,
        token: str,
        image: UploadFile,
    ) -> QwenUploadData:
        data: QwenResponse = await self._core.post(
            token=token,
            # **kwargs
            endpoint=QwenEndpoint.MEDIA_TOKEN,
            body=IPhotoBody(
                filesize=image.size,
            ),
        )

        return data.resp

    async def __get_account_token(
        self,
        account: QwenAccounts,
    ) -> str:
        token_data: QwenAccountsTokens = (
            await account_token_database.fetch_with_filters(
                account_id=account.id,
            )
        )

        token = token_data.jwt_token

        if token is None:
            token: str = await self.auth_user_account(account)

            await update_account_token(
                account,
                token,
                project=AccountProjectToken.QWEN,
            )

        return token

    async def __reauthenticate(
        self,
        account: QwenAccounts,
    ) -> str:
        return await self.auth_user_account(
            account,
        )

    async def __generate_new_chat(
        self,
        token: str,
    ) -> str:
        data: QwenResponse | QwenErrorResponse = await self._core.post(
            token=token,
            # Request **kwargs
            endpoint=QwenEndpoint.CHAT,
            body=IQwenChat(),
        )

        if not isinstance(data, QwenResponse):
            raise HTTPException(
                status_code=400,
                detail=data.detail,
            )

        return data.resp.id

    async def __generate_photo(
        self,
        token: str,
        chat_id: str,
        body: IT2IBody,
    ) -> str:
        child_id: str = str(uuid4())

        request_body: IQwenPhotoBody = IQwenPhotoBody(
            chat_id=chat_id,
            size=body.media_size,
            messages=[
                IQwenChatMessage(
                    content=body.prompt,
                    children_ids=[child_id],
                )
            ],
        )

        await self._core.post(
            token=token,
            is_serialized=False,
            # Request **kwargs
            endpoint=QwenEndpoint.GENERATE.format(
                chat_id=chat_id,
            ),
            body=request_body,
        )

        return child_id

    async def __fetch_photo_url(
        self,
        token: str,
        chat_id: str,
    ) -> QwenPhotoAPIResponse:
        data: QwenResponse | QwenErrorResponse = await self._core.get(
            token=token,
            # Request **kwargs
            endpoint=QwenEndpoint.RESULT.format(
                chat_id=chat_id,
            ),
        )

        if not isinstance(data, QwenResponse):
            raise HTTPException(
                status_code=400,
                detail=data.detail,
            )

        media_url: str = self.__get_media_content(data)

        return QwenPhotoAPIResponse(
            media_url=media_url,
        )

    async def text_to_photo(
        self,
        body: IT2IBody,
    ) -> QwenPhotoAPIResponse:
        account = await account_database.fetch_next_account()

        # account_id = account.id

        max_attempts = 1

        last_err_code = None

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> QwenPhotoAPIResponse:
                    chat_id: str = await self.__generate_new_chat(
                        token=token,
                    )

                    await self.__generate_photo(
                        token=token,
                        chat_id=chat_id,
                        body=body,
                    )

                    return await self.__fetch_photo_url(
                        token=token,
                        chat_id=chat_id,
                    )

                data: QwenPhotoAPIResponse = await call(token)

                # if not data.detail:
                #     return await self.__handle_success(
                #         data,
                #         account_id,
                #         body,
                #     )
                return data

                # raise HTTPException(
                #     status_code=400,
                #     detail=data.detail,
                # )

                # last_err_code = data.resp.status

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.TOPMEDIA,
                    )

                    try:
                        data = await call(token)

                        # if not data.detail:
                        # # return await self.__handle_success(
                        # #     data,
                        # #     account_id,
                        # #     body,
                        # # )
                        return data
                    except Exception as final_err:
                        raise final_err
                    # return await self.__handle_failure()
                await sleep(1)

        return await self.__handle_failure(
            400,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    # async def photo_to_video(
    #     self,
    #     image: UploadFile,
    #     body: IT2IBody,
    # ) -> QwenPhotoAPIResponse:
    #     account = await account_database.fetch_next_account()

    #     # account_id = account.id

    #     max_attempts = 1

    #     last_err_code = None

    #     for attempt in range(max_attempts):
    #         token = await self.__get_account_token(
    #             account,
    #         )
    #         file_bytes: bytes = await image.read()

    #         try:

    #             async def call(
    #                 token: str,
    #             ) -> QwenPhotoAPIResponse:
    #                 bucket_data: QwenUploadData = await self.__fetch_upload_token(
    #                     token,
    #                     image,
    #                 )

    #                 await upload_qwen_file(
    #                     bucket_data,
    #                     file_bytes,
    #                 )

    #                 return await self.__fetch_photo_url(
    #                     token=token,
    #                     chat_id=chat_id,
    #                 )

    #             data: QwenPhotoAPIResponse = await call(token)

    #             # if not data.detail:
    #             #     return await self.__handle_success(
    #             #         data,
    #             #         account_id,
    #             #         body,
    #             #     )
    #             return data

    #             # raise HTTPException(
    #             #     status_code=400,
    #             #     detail=data.detail,
    #             # )

    #             # last_err_code = data.resp.status

    #         except Exception:
    #             if attempt == max_attempts - 1:
    #                 token = await self.__reauthenticate(account)

    #                 await update_account_token(
    #                     account,
    #                     token,
    #                     project=AccountProjectToken.TOPMEDIA,
    #                 )

    #                 try:
    #                     data = await call(token)

    #                     # if not data.detail:
    #                     # # return await self.__handle_success(
    #                     # #     data,
    #                     # #     account_id,
    #                     # #     body,
    #                     # # )
    #                     return data
    #                 except Exception as final_err:
    #                     raise final_err
    #                 # return await self.__handle_failure()
    #             await sleep(1)

    #     return await self.__handle_failure(
    #         400,
    #         extra={
    #             "Данные аккаунта": {
    #                 "логин": account.username,
    #                 "пароль": account.password,
    #             }
    #         },
    #     )
