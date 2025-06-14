# coding utf-8

from fastapi import UploadFile

from .core import PixverseCore

from functools import lru_cache

from ....domain.conf import app_conf

from ....domain.errors import PixverseError

from ....domain.entities.core import IConfEnv

from ...orm.database.repositories import (
    PixverseAccountRepository,
    PixverseStyleRepository,
    PixverseTemplateRepository,
)

from ....domain.repositories import IDatabase

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
    ) -> AuthRes:
        account = await account_database.fetch_next_account()
        data: Response = await self._core.post(
            endpoint=PixverseEndpoint.AUTH,
            body=UserCredentials(
                username=account.username,
                password=account.password,
            ),
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
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
            raise PixverseError(
                status_code=data.err_code,
            )
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
            raise PixverseError(
                status_code=data.err_code,
            )
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
            raise PixverseError(
                status_code=data.err_code,
            )
        return True

    async def generation_status(
        self,
        id: int,
    ) -> GenerationStatus:
        user: AuthRes = await self.auth_user()

        data: Response = await self._core.post(
            token=user.access_token,
            endpoint=PixverseEndpoint.STATUS,
            body=StatusBody(),
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
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
            raise PixverseError(
                status_code=data.err_code,
            )
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
            raise PixverseError(
                status_code=data.err_code,
            )
        return data.resp.items

    async def fetch_templates(
        self,
    ) -> EffectResponse:
        data: Response = await self._core.post(
            endpoint=PixverseEndpoint.TEMPLATES,
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        return data.resp

    async def text_to_video(
        self,
        body: T2VBody,
    ) -> Resp:
        user: AuthRes = await self.auth_user()

        data: Response = await self._core.post(
            token=user.access_token,
            endpoint=PixverseEndpoint.TEXT,
            body=IT2VBody(
                prompt=body.prompt,
            ),
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        return data.resp

    async def image_to_video(
        self,
        body: I2VBody,
        image: UploadFile,
    ) -> Resp:
        user: AuthRes = await self.auth_user()

        token_data: UTResp = await self.upload_token(
            user.access_token,
        )

        image_bytes: bytes = await image.read()

        await upload_file(
            image_bytes,
            image.filename,
            **token_data.dict,
        )

        await self.upload_image(
            user.access_token,
            image.filename,
            size=len(image_bytes),
        )

        data = await self._core.post(
            token=user.access_token,
            endpoint=PixverseEndpoint.IMAGE,
            body=II2VBody(
                img_path=image.filename,
                img_url=image.filename,
                prompt=body.prompt,
            ),
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        return data.resp

    async def restyle_video(
        self,
        body: R2VBody,
        video: UploadFile,
    ):
        user: AuthRes = await self.auth_user()

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
            video.filename,
            **token_data.dict,
        )

        await self.upload_video(
            user.access_token,
            video.filename,
            video.filename,
        )

        frame_data = await self._core.post(
            token=user.access_token,
            endpoint=PixverseEndpoint.LAST_FRAME,
            body=LFBody(
                video_path=video.filename,
            ),
        )

        data: Response = await self._core.post(
            token=user.access_token,
            endpoint=PixverseEndpoint.RESTYLE,
            body=IRVBody(
                video_path=video.filename,
                video_url=video.filename,
                video_duration=5,
                restyle_prompt=style.prompt,
                last_frame_url=frame_data.resp.last_frame,
            ),
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        return data.resp

    async def template_video(
        self,
        body: TE2VBody,
        image: UploadFile,
    ):
        user: AuthRes = await self.auth_user()

        token_data: UTResp = await self.upload_token(
            user.access_token,
        )
        image_bytes: bytes = await image.read()

        template: Template | None = await templates_database.fetch_template(
            "template_id",
            body.template_id,
        )

        print(template)

        await upload_file(
            image_bytes,
            image.filename,
            **token_data.dict,
        )

        await self.upload_image(
            user.access_token,
            image.filename,
            size=len(image_bytes),
        )

        data: Response = await self._core.post(
            token=user.access_token,
            endpoint=PixverseEndpoint.IMAGE,
            body=IIT2VBody(
                img_path=image.filename,
                img_url=image.filename,
                prompt=template.prompt,
                template_id=body.template_id,
            ),
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        return data.resp
