# coding utf-8

from fastapi import UploadFile

from ......infrastructure.external.calories import CaloriesClient


class CaloriesController:
    def __init__(
        self,
        client: CaloriesClient,
    ) -> None:
        self._client = client

    async def text_to_calories(
        self,
        description: str,
    ):
        return await self._client.text_to_calories(
            description,
        )

    async def photo_to_calories(
        self,
        image: UploadFile,
    ):
        return await self._client.photo_to_calories(
            image,
        )
