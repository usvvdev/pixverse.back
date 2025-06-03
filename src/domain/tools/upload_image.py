# coding utf-8

from oss2 import StsAuth, Bucket

import os

import uuid

from fastapi import UploadFile, HTTPException

from ..constants import (
    BUCKET_URL,
    BUCKET_NAME,
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


ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "video/mp4",
    "video/mov",
    "video/quicktime",
}

UPLOAD_DIR = "uploads"


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
