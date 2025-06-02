# coding utf-8

from fastapi import UploadFile

from fastapi.security import OAuth2PasswordRequestForm

from .....domain.entities.pixverse import IBody

from .....interface.schemas.external import (
    T2VBody,
    Resp,
    AuthRes,
    GenBody,
    TemplateBody,
    TokensResponse,
    GenerationStatus,
    Template,
    EffectResponse,
)

from .....interface.controllers.api.v1 import PixVerseController


class PixVerseView:
    def __init__(
        self,
        controller: PixVerseController,
    ) -> None:
        self._controller = controller

    async def auth_user(
        self,
        body: OAuth2PasswordRequestForm,
    ) -> AuthRes:
        return await self._controller.auth_user(
            body,
        )

    async def text_to_video(
        self,
        body: T2VBody,
        token: str,
    ) -> Resp:
        return await self._controller.text_to_video(
            body,
            token,
        )

    async def image_to_video(
        self,
        body: IBody,
        image: UploadFile,
        token: str,
    ) -> Resp:
        return await self._controller.image_to_video(
            body,
            image,
            token,
        )

    async def generation_status(
        self,
        body: GenBody,
        token: str,
    ) -> GenerationStatus:
        return await self._controller.generation_status(
            body,
            token,
        )

    async def credits_amount(
        self,
        token: str,
    ) -> TokensResponse:
        return await self._controller.credits_amount(
            token,
        )

    async def restyle_templates(
        self,
        body: TemplateBody,
    ) -> list[Template]:
        return await self._controller.restyle_templates(
            body,
        )

    async def effect_templates(
        self,
    ) -> EffectResponse:
        return await self._controller.effect_templates()
