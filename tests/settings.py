import importlib
from pydantic_settings import BaseSettings
import app.core.config


class TestSettings(BaseSettings):

    DB_HOST: str = "dummy"
    DB_NAME: str = "dummy"
    DB_USER: str = "dummy"
    DB_PASSWORD: str = "dummy"
    DB_PORT: int = 5432

    REDIS_HOST: str = "dummy"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    REDIS_URL_EXPIRES: int = 900

    REDIS_URL: str = "dummy"

    SECRET_KEY: str = "dummy"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    GOOGLE_CODING_API_KEY: str = "dummy"

    AWS_ACCESS_KEY_ID: str = "dummy"
    AWS_SECRET_ACCESS_KEY: str = "dummy"
    AWS_REGION: str = "dummy"
    AWS_S3_BUCKET: str = "dummy"
    AWS_S3_PRESIGNED_UPLOAD_EXPIRES_IN: int = 300
    AWS_S3_PRESIGNED_READ_EXPIRES_IN: int = 3600

    API_PREFIX: str = "/api/v0"


def apply_test_settings():
    app.core.config.Settings = TestSettings
    app.core.config.settings = TestSettings()
    importlib.reload(app.core.config)
