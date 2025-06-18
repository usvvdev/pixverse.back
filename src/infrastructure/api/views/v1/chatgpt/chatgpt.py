# coding utf-8

from fastapi import UploadFile

from ......domain.entities.chatgpt import IBody, T2PBody, TB2PBody

from ......interface.controllers.api.v1 import ChatGPTController


class ChatGPTView:
    def __init__(
        self,
        controller: ChatGPTController,
    ) -> None:
        self._controller = controller

    async def text_to_photo(
        self,
        body: IBody,
    ):
        return await self._controller.text_to_photo(
            body,
        )

    async def photo_to_photo(
        self,
        body: IBody,
        image: UploadFile,
    ):
        return await self._controller.photo_to_photo(
            body,
            image,
        )

    async def template_to_photo(
        self,
        body: T2PBody,
        image: UploadFile,
    ):
        return await self._controller.template_to_photo(
            body,
            image,
        )

    async def template_toybox_to_photo(
        self,
        body: TB2PBody,
        image: UploadFile,
    ):
        return await self._controller.template_toybox_to_photo(
            body,
            image,
        )
