# coding utf-8

import os

import uuid

from typing import Any

from base64 import b64decode

from io import BytesIO

from PIL import Image

from pillow_heif import register_heif_opener

from oss2 import StsAuth, Bucket

from fastapi import UploadFile, HTTPException

from ..entities.chatgpt import IFile

from ..constants import (
    BUCKET_URL,
    BUCKET_NAME,
    ALLOWED_MIME_TYPES,
    UPLOAD_DIR,
)


async def upload_file(
    image_bytes: bytes,
    filename: str,
    access_key_id: str,
    access_key_secret: str,
    security_token: str,
) -> bool:
    bucket = Bucket(
        StsAuth(access_key_id, access_key_secret, security_token),
        BUCKET_URL,
        bucket_name=BUCKET_NAME,
    )
    return bucket.put_object(
        f"upload/{filename}",
        image_bytes,
    )


async def convert_heic_to_jpg(
    image_bytes: bytes,
) -> tuple[bytes, str]:
    register_heif_opener()

    image = Image.open(
        BytesIO(
            image_bytes,
        )
    ).convert("RGB")

    buffer = BytesIO()

    image.save(buffer, format="JPEG")
    return buffer.getvalue(), ".jpg"


def save_upload_file(
    file: UploadFile,
    subdir: str = "",
) -> str | None:
    if file is None:
        return None

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400, detail=f"Недопустимий тип файлу: {file.content_type}"
        )

    os.makedirs(os.path.join(UPLOAD_DIR, subdir), exist_ok=True)
    ext = os.path.splitext(file.filename)[-1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(UPLOAD_DIR, subdir, unique_name)

    with open(save_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)

    return save_path


async def upload_chatgpt_file(
    body: Any,
    image: UploadFile,
) -> dict[str, Any]:
    return IFile(
        model=(None, "gpt-image-1"),
        image=(image.filename, await image.read(), image.content_type),
        prompt=(None, body.prompt),
    ).dict


def b64_json_to_image(
    b64_string: str,
):
    os.makedirs(os.path.join(UPLOAD_DIR, "photo"), exist_ok=True)
    image_bytes = b64decode(b64_string)

    image = Image.open(BytesIO(image_bytes))

    unique_name = f"{uuid.uuid4()}.jpg"

    save_path = os.path.join(UPLOAD_DIR, "photo", unique_name)

    image.save(save_path)

    return save_path
