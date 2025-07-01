# coding utf-8

from fastapi import Response

from starlette.requests import Request

from starlette.middleware.base import BaseHTTPMiddleware

from starlette.responses import PlainTextResponse


class LimitUploadSize(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        max_upload_size: int = 1024 * 1024 * 20,
    ) -> None:
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> PlainTextResponse | Response:
        content_length: str | None = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_upload_size:
            return PlainTextResponse("File too large", status_code=413)
        return await call_next(request)
