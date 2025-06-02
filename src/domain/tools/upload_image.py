# coding utf-8

from oss2 import StsAuth, Bucket

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
