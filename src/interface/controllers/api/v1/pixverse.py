# coding utf-8

from fastapi import UploadFile

from fastapi.security import OAuth2PasswordRequestForm

from ....schemas.external import (
    Resp,
    T2VBody,
    R2VBody,
    GenBody,
    AuthRes,
    GenerationStatus,
    TemplateBody,
    EffectResponse,
    Template,
    TokensResponse,
    TE2VBody,
)

from .....infrastructure.external.pixverse import PixVerseClient


class PixVerseController:
    def __init__(
        self,
        client: PixVerseClient,
    ) -> None:
        self._client = client

    async def text_to_video(
        self,
        body: T2VBody,
    ) -> Resp:
        return await self._client.text_to_video(
            body,
        )

    async def image_to_video(
        self,
        body: T2VBody,
        image: UploadFile,
    ) -> Resp:
        return await self._client.image_to_video(
            body,
            image,
        )

    async def generation_status(
        self,
        id: int,
    ) -> GenerationStatus:
        return await self._client.generation_status(
            id,
        )

    async def restyle_video(
        self,
        body: R2VBody,
        image: UploadFile,
    ) -> Resp:
        return await self._client.restyle_video(
            body,
            image,
        )

    async def template_video(
        self,
        body: TE2VBody,
        image: UploadFile,
    ) -> Resp:
        return await self._client.template_video(
            body,
            image,
        )

    # async def credits_amount(
    #     self,
    #     token: str,
    # ) -> TokensResponse:
    #     return await self._client.credits_amount(
    #         token,
    #     )

    # async def restyle_templates(
    #     self,
    #     body: TemplateBody,
    # ) -> list[Template]:
    #     return await self._client.restyle_templates(
    #         body,
    #     )

    # async def effect_templates(
    #     self,
    # ) -> EffectResponse:
    #     return await self._client.effect_templates()
