import boto3

from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from io import BytesIO
from botocore.client import Config
from botocore.exceptions import ClientError

from app.core.config import settings
from app.core.exceptions.domain_exception import S3PresignedUrlError


@dataclass
class PresignedUpload:
    upload_url: str
    method: str
    expires_at: datetime


@dataclass
class PresignedRead:
    url: str
    method: str
    expires_at: datetime


class S3Service:

    def __init__(self) -> None:
        self._client = boto3.client(
            "s3",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(
                signature_version="s3v4",
                retries={"max_attempts": 3},
            ),
        )
        self._bucket: str = settings.AWS_S3_BUCKET
        self._upload_expires_in: int = settings.AWS_S3_PRESIGNED_UPLOAD_EXPIRES_IN
        self._read_expires_in: int = settings.AWS_S3_PRESIGNED_READ_EXPIRES_IN

    # -----------------------------------------------
    # PRESIGNED UPLOAD
    # -----------------------------------------------

    def generate_presigned_upload_url(
        self, *, storage_key: str, content_type: str, expires_in: int | None = None
    ) -> PresignedUpload:

        expires_in = expires_in or self._upload_expires_in
        try:
            upload_url = self._client.generate_presigned_url(
                ClientMethod="put_object",
                Params={
                    "Bucket": self._bucket,
                    "Key": storage_key,
                    "ContentType": content_type,
                },
                ExpiresIn=expires_in,
                HttpMethod="PUT",
            )
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
            return PresignedUpload(upload_url=upload_url, method="PUT", expires_at=expires_at)

        except ClientError as exc:
            raise S3PresignedUrlError(f"Failed to generate presigned upload URL for {storage_key}") from exc

    # -----------------------------------------------
    # PRESIGNED READ
    # -----------------------------------------------

    def generate_presigned_read_url(self, *, storage_key: str, expires_in: int | None = None) -> PresignedRead:

        expires_in = expires_in or self._read_expires_in
        try:
            read_url = self._client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self._bucket, "Key": storage_key},
                ExpiresIn=expires_in,
                HttpMethod="GET",
            )
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
            return PresignedRead(url=read_url, method="GET", expires_at=expires_at)

        except ClientError as exc:
            raise S3PresignedUrlError(f"Failed to generate presigned read URL for {storage_key}") from exc

    def get_object_bytes(self, storage_key: str) -> bytes:
        obj = self._client.get_object(Bucket=self._bucket, Key=storage_key)
        return obj["Body"].read()

    def put_object_bytes(self, storage_key: str, data: BytesIO, content_type: str):
        try:
            data.seek(0)
            self._client.put_object(
                Bucket=self._bucket,
                Key=storage_key,
                Body=data,
                ContentType=content_type,
            )
            return True
        except ClientError as exc:
            raise S3PresignedUrlError(f"Failed to read object {storage_key}") from exc

    def exists(self, storage_key: str) -> bool:
        try:
            self._client.head_object(Bucket=self._bucket, Key=storage_key)
            return True
        except ClientError:
            return False

    # -----------------------------------------------
    # PRESIGNED DELETE
    # -----------------------------------------------

    def delete(self, *, storage_key: str) -> None:
        self._client.delete_object(Bucket=self._bucket, Key=storage_key)
