# coding utf-8

from fastapi import UploadFile

from fastapi.security import OAuth2PasswordRequestForm

from .....domain.entities.pixverse import IBody

from .....interface.schemas.external import (
    T2VBody,
    Resp,
    R2VBody,
    AuthRes,
    GenBody,
    TemplateBody,
    TokensResponse,
    GenerationStatus,
    Template,
    EffectResponse,
    TE2VBody,
)

from .....interface.controllers.api.v1 import PixVerseController


class PixVerseView:
    def __init__(
        self,
        controller: PixVerseController,
    ) -> None:
        self._controller = controller

    async def text_to_video(
        self,
        body: T2VBody,
    ) -> Resp:
        return await self._controller.text_to_video(
            body,
        )

    async def image_to_video(
        self,
        body: IBody,
        image: UploadFile,
    ) -> Resp:
        return await self._controller.image_to_video(
            body,
            image,
        )

    async def restyle_video(
        self,
        body: R2VBody,
        video: UploadFile,
    ) -> Resp:
        return await self._controller.restyle_video(
            body,
            video,
        )

    async def template_video(
        self,
        body: TE2VBody,
        image: UploadFile,
    ) -> Resp:
        return await self._controller.template_video(
            body,
            image,
        )

    async def generation_status(
        self,
        id: int,
    ) -> GenerationStatus:
        return await self._controller.generation_status(
            id,
        )

    # async def credits_amount(
    #     self,
    #     token: str,
    # ) -> TokensResponse:
    #     return await self._controller.credits_amount(
    #         token,
    #     )

    # async def restyle_templates(
    #     self,
    #     body: TemplateBody,
    # ) -> list[Template]:
    #     return await self._controller.restyle_templates(
    #         body,
    #     )

    # async def effect_templates(
    #     self,
    # ) -> EffectResponse:
    #     return await self._controller.effect_templates()
