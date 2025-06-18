# coding utf-8

from fastapi import UploadFile

from ......domain.entities.chatgpt import (
    IBody,
    T2PBody,
    TB2PBody,
)

from ......infrastructure.external.chatgpt import ChatGPTClient


class ChatGPTController:
    def __init__(
        self,
        client: ChatGPTClient,
    ) -> None:
        self._client = client

    async def text_to_photo(
        self,
        body: IBody,
    ):
        return await self._client.text_to_photo(
            body,
        )

    async def photo_to_photo(
        self,
        body: IBody,
        image: UploadFile,
    ):
        return await self._client.photo_to_photo(
            body,
            image,
        )

    async def template_to_photo(
        self,
        body: T2PBody,
        image: UploadFile,
    ):
        return await self._client.template_to_photo(
            body,
            image,
        )

    async def template_toybox_to_photo(
        self,
        body: TB2PBody,
        image: UploadFile,
    ):
        return await self._client.photo_to_photo(
            IBody(
                user_id=body.user_id,
                app_id=body.app_id,
                prompt=f"Создай игрушку по моему фото в формате экшн-фигурки. Фигурка должна быть в полный рост и помещаться внутри {body.box_color} коробки в левой части, справа рядом размести ее аксессуары: {body.in_box}. На верхней части коробки напиши {body.box_name}. Изображение должно быть максимально реалистичным",
            ),
            image,
        )
