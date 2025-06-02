# coding utf-8

from fastapi import UploadFile

from fastapi.security import OAuth2PasswordRequestForm

from .core import PixverseCore

from ....domain.conf import app_conf

from ....domain.errors import PixverseError

from ....domain.entities.core import IConfEnv

from ....domain.entities.pixverse import IBody

from ....domain.tools import upload_file

from ....interface.schemas.external import (
    AuthRes,
    UserCredentials,
    Response,
    T2VBody,
    IMGBody,
    I2VBody,
    V2VBody,
    StatusBody,
    UploadIMG,
    Resp,
    UTResp,
    GenerationStatus,
    GenBody,
    TemplateBody,
    TokensResponse,
    EffectResponse,
    Template,
)

from ....domain.typing.enums import PixverseEndpoint


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
        core: PixverseCore,
    ) -> None:
        self._core = core

    async def auth_user(
        self,
        body: OAuth2PasswordRequestForm,
    ) -> AuthRes:
        data: Response = await self._core.post(
            endpoint=PixverseEndpoint.AUTH,
            body=UserCredentials(
                **body.__dict__,
            ),
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        return data.resp.result

    async def text_to_video(
        self,
        body: T2VBody,
        token: str,
    ) -> Resp:
        data: Response = await self._core.post(
            token=token,
            endpoint=PixverseEndpoint.TEXT,
            body=body,
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        return data.resp

    async def upload_token(
        self,
    ) -> UTResp:
        data: Response = await self._core.post(
            endpoint=PixverseEndpoint.UPLOAD_TOKEN,
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        return data.resp

    async def upload_image(
        self,
        filename: str,
        size: int,
    ) -> bool:
        data: Response = await self._core.post(
            PixverseEndpoint.UPLOAD_IMAGE,
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
        filename: str,
        size: int,
    ) -> bool:
        data: Response = await self._core.post(
            PixverseEndpoint.UPLOAD_VIDEO,
            body="",
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        return True

    async def image_to_video(
        self,
        body: IBody,
        image: UploadFile,
        token: str,
    ) -> Resp:
        token_data: UTResp = await self.upload_token()

        image_bytes: bytes = await image.read()

        await upload_file(
            image_bytes,
            image.filename,
            **token_data.dict,
        )

        await self.upload_image(
            image.filename,
            size=len(image_bytes),
        )

        data: Response = await self._core.post(
            token=token,
            endpoint=PixverseEndpoint.IMAGE,
            body=I2VBody(
                img_path=image.filename,
                img_url=image.filename,
                **body.dict,
            ),
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        return data.resp

    async def generation_status(
        self,
        body: GenBody,
        token: str,
    ) -> GenerationStatus:
        data: Response = await self._core.post(
            token=token,
            endpoint=PixverseEndpoint.STATUS,
            body=StatusBody(),
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        for video in data.resp.data:
            if video.video_id == body.video_id:
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

    async def restyle_templates(
        self,
        body: TemplateBody,
    ) -> list[Template]:
        data: Response = await self._core.post(
            endpoint=PixverseEndpoint.RESTYLE_TEMPLATE,
            body=body,
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        return data.resp.items

    async def effect_templates(
        self,
    ) -> EffectResponse:
        data: Response = await self._core.post(
            endpoint=PixverseEndpoint.EFFECT,
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        return data.resp

    async def restyle_video(
        self,
        body: V2VBody,
        video: UploadFile,
        token: str,
    ):
        token_data: UTResp = await self.upload_token()

        video_bytes: bytes = await video.read()

        await upload_file(
            video_bytes,
            video.filename,
            **token_data.dict,
        )

        await self.upload_video(
            video.filename,
        )

        data: Response = await self._core.post(
            token=token,
            endpoint=PixverseEndpoint.RESTYLE,
            body=V2VBody(
                video_path=video.filename,
                video_url=video.filename,
            ),
        )
        if data.err_code != 0:
            raise PixverseError(
                status_code=data.err_code,
            )
        return data.resp
