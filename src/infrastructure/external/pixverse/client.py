# coding utf-8

from fastapi import UploadFile

from .core import PixverseCore

from uuid import uuid4

from ....domain.conf import app_conf

from ....domain.errors import PixverseError

from ....domain.entities.core import (
    IConfEnv,
)

from ...orm.database.repositories import (
    PixverseAccountRepository,
    PixverseStyleRepository,
    PixverseTemplateRepository,
    UserGenerationRepository,
)

from ....domain.repositories import IDatabase

from ....domain.entities.bot import IBotReporter

from ....domain.entities.pixverse import (
    IT2VBody,
    II2VBody,
    IIT2VBody,
    IRVBody,
    LFBody,
)

from ....domain.tools import upload_file

from ....interface.schemas.external import (
    AuthRes,
    UserCredentials,
    Response,
    T2VBody,
    R2VBody,
    TE2VBody,
    I2VBody,
    IMGBody,
    VideoBody,
    StatusBody,
    UploadIMG,
    Resp,
    UTResp,
    GenerationStatus,
    TemplateBody,
    TokensResponse,
    EffectResponse,
    TemplateResp,
    GenerationData,
)

from ....interface.schemas.api import Style, Template

from ....domain.typing.enums import PixverseEndpoint


conf: IConfEnv = app_conf()


account_database = PixverseAccountRepository(
    engine=IDatabase(conf),
)

style_database = PixverseStyleRepository(
    engine=IDatabase(conf),
)

templates_database = PixverseTemplateRepository(
    engine=IDatabase(conf),
)

user_generations_database = UserGenerationRepository(
    engine=IDatabase(conf),
)

telegram_bot = IBotReporter(
    conf,
)


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
        core: PixverseCore,
    ) -> None:
        self._core = core

    async def auth_user(
        self,
        account,
    ) -> AuthRes:
        data: Response = await self._core.post(
            endpoint=PixverseEndpoint.AUTH,
            body=UserCredentials(
                username=account.username,
                password=account.password,
            ),
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            await telegram_bot.send_error(error=error)

            raise error
        return data.resp.result

    async def upload_token(
        self,
        token: str,
    ) -> UTResp:
        data: Response = await self._core.post(
            token=token,
            endpoint=PixverseEndpoint.UPLOAD_TOKEN,
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            await telegram_bot.send_error_message(error=error)

            raise error
        return data.resp

    async def upload_image(
        self,
        token: str,
        filename: str,
        size: int,
    ) -> bool:
        data: Response = await self._core.post(
            token=token,
            endpoint=PixverseEndpoint.UPLOAD_IMAGE,
            body=IMGBody(
                images=[
                    UploadIMG(name=filename, size=size, path=f"upload/{filename}").dict
                ]
            ),
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            await telegram_bot.send_error_message(error=error)

            raise error
        return True

    async def upload_video(
        self,
        token: str,
        filename: str,
        path: int,
    ) -> bool:
        data: Response = await self._core.post(
            token=token,
            endpoint=PixverseEndpoint.UPLOAD_VIDEO,
            body=VideoBody(
                name=filename,
                path=path,
            ),
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            await telegram_bot.send_error_message(error=error)

            raise error
        return True

    async def generation_status(
        self,
        id: int,
    ) -> GenerationStatus:
        generation_data = await user_generations_database.fetch_generation(
            "generation_id", id
        )

        account = await account_database.fetch_account(
            "id",
            generation_data.account_id,
        )

        user: AuthRes = await self.auth_user(account)

        data: Response = await self._core.post(
            token=user.access_token,
            endpoint=PixverseEndpoint.STATUS,
            body=StatusBody(),
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            await telegram_bot.send_error_message(error=error)

            raise error
        for video in data.resp.data:
            if video.video_id == id:
                if video.video_status == 1 and video.first_frame:
                    return GenerationStatus(status="success", video_url=video.url)
                return GenerationStatus(
                    status="generating" if video.video_status == 10 else "error"
                )

    async def credits_amount(
        self,
        token: str,
    ) -> TokensResponse:
        data: Response = await self._core.get(
            token=token,
            endpoint=PixverseEndpoint.TOKEN,
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            await telegram_bot.send_error_message(error=error)

            raise error
        return data.resp

    async def fetch_styles(
        self,
        body: TemplateBody,
    ) -> list[TemplateResp]:
        data: Response = await self._core.post(
            endpoint=PixverseEndpoint.RESTYLE_TEMPLATE,
            body=body,
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            await telegram_bot.send_error_message(error=error)

            raise error
        return data.resp.items

    async def fetch_templates(
        self,
    ) -> EffectResponse:
        data: Response = await self._core.post(
            endpoint=PixverseEndpoint.TEMPLATES,
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            await telegram_bot.send_error_message(error=error)

            raise error
        return data.resp

    async def text_to_video(
        self,
        body: T2VBody,
    ) -> Resp:
        account = await account_database.fetch_next_account()

        account_id = account.id

        user: AuthRes = await self.auth_user(account)

        data: Response = await self._core.post(
            token=user.access_token,
            endpoint=PixverseEndpoint.TEXT,
            body=IT2VBody(
                prompt=body.prompt,
            ),
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            context = f"Account data: \n {account.username} \n {account.password}"
            await telegram_bot.send_error_message(
                error=error,
                context=context,
            )

            raise error
        await user_generations_database.add_record(
            GenerationData(
                generation_id=data.resp.video_id,
                account_id=account_id,
                user_id=body.user_id,
                app_id=body.app_id,
            )
        )
        return data.resp

    async def image_to_video(
        self,
        body: I2VBody,
        image: UploadFile,
    ) -> Resp:
        account = await account_database.fetch_next_account()

        account_id = account.id

        filename = str(uuid4())

        user: AuthRes = await self.auth_user(account)

        token_data: UTResp = await self.upload_token(
            user.access_token,
        )

        image_bytes: bytes = await image.read()

        await upload_file(
            image_bytes,
            filename,
            **token_data.dict,
        )

        await self.upload_image(
            user.access_token,
            filename,
            size=len(image_bytes),
        )

        data = await self._core.post(
            token=user.access_token,
            endpoint=PixverseEndpoint.IMAGE,
            body=II2VBody(
                img_path=filename,
                img_url=filename,
                prompt=body.prompt,
            ),
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            context = f"Account data: \n {account.username} \n {account.password}"
            await telegram_bot.send_error_message(
                error=error,
                context=context,
            )

            raise error
        await user_generations_database.add_record(
            GenerationData(
                generation_id=data.resp.video_id,
                account_id=account_id,
                user_id=body.user_id,
                app_id=body.app_id,
            )
        )
        return data.resp

    async def restyle_video(
        self,
        body: R2VBody,
        video: UploadFile,
    ):
        account = await account_database.fetch_next_account()

        account_id = account.id

        filename = str(uuid4())

        user: AuthRes = await self.auth_user(account)

        token_data: UTResp = await self.upload_token(
            user.access_token,
        )

        video_bytes: bytes = await video.read()

        style: Style | None = await style_database.fetch_style(
            "template_id",
            body.template_id,
        )

        await upload_file(
            video_bytes,
            filename,
            **token_data.dict,
        )

        await self.upload_video(
            user.access_token,
            filename,
            filename,
        )

        frame_data = await self._core.post(
            token=user.access_token,
            endpoint=PixverseEndpoint.LAST_FRAME,
            body=LFBody(
                video_path=filename,
            ),
        )

        data: Response = await self._core.post(
            token=user.access_token,
            endpoint=PixverseEndpoint.RESTYLE,
            body=IRVBody(
                video_path=filename,
                video_url=filename,
                video_duration=5,
                restyle_prompt=style.prompt,
                last_frame_url=frame_data.resp.last_frame,
            ),
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            context = f"Account data: \n {account.username} \n {account.password}"
            await telegram_bot.send_error_message(
                error=error,
                context=context,
            )

            raise error
        await user_generations_database.add_record(
            GenerationData(
                generation_id=data.resp.video_id,
                account_id=account_id,
                user_id=body.user_id,
                app_id=body.app_id,
            )
        )
        return data.resp

    async def template_video(
        self,
        body: TE2VBody,
        image: UploadFile,
    ):
        account = await account_database.fetch_next_account()

        account_id = account.id

        filename = str(uuid4())

        user: AuthRes = await self.auth_user(account)

        token_data: UTResp = await self.upload_token(
            user.access_token,
        )
        image_bytes: bytes = await image.read()

        template: Template | None = await templates_database.fetch_template(
            "template_id",
            body.template_id,
        )

        await upload_file(
            image_bytes,
            filename,
            **token_data.dict,
        )

        await self.upload_image(
            user.access_token,
            filename,
            size=len(image_bytes),
        )

        data: Response = await self._core.post(
            token=user.access_token,
            endpoint=PixverseEndpoint.IMAGE,
            body=IIT2VBody(
                img_path=filename,
                img_url=filename,
                prompt=template.prompt,
                template_id=body.template_id,
            ),
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            context = f"Account data: \n {account.username} \n {account.password}"
            await telegram_bot.send_error_message(
                error=error,
                context=context,
            )

            raise error
        await user_generations_database.add_record(
            GenerationData(
                generation_id=data.resp.video_id,
                account_id=account_id,
                user_id=body.user_id,
                app_id=body.app_id,
            )
        )
        return data.resp
