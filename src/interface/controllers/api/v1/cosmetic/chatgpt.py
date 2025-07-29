# coding utf-8

from fastapi import UploadFile

from ......infrastructure.external.cosmetic import CosmeticClient

from ......interface.schemas.external import ChatGPTCosmetic


class CosmeticController:
    def __init__(
        self,
        client: CosmeticClient,
    ) -> None:
        self._client = client

    async def text_to_cosmetic(
        self,
        description: str,
    ) -> list[ChatGPTCosmetic]:
        return await self._client.text_to_cosmetic(
            description,
        )

    async def photo_to_cosmetic(
        self,
        image: UploadFile,
    ) -> list[ChatGPTCosmetic]:
        return await self._client.photo_to_cosmetic(
            image,
        )
