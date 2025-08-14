# coding utf-8

from fastapi import UploadFile

from ......domain.entities.qwen import IT2IBody

from .....schemas.external import QwenPhotoAPIResponse

from ......infrastructure.external.qwen import QwenClient


class QwenController:
    def __init__(
        self,
        client: QwenClient,
    ) -> None:
        self._client = client

    async def text_to_photo(
        self,
        body: IT2IBody,
    ) -> QwenPhotoAPIResponse:
        return await self._client.text_to_photo(
            body,
        )

    async def fetch_upload_token(
        self,
        token: str,
        image: UploadFile,
    ):
        return await self._client.fetch_upload_token(
            token,
            image,
        )
