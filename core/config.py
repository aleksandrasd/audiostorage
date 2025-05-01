import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    AUDIO_FORMATS: list[str] = ['wav', 'mp3']
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    BUCKET_NAME: str = "audio"
    WRITER_DB_URL: (
        str
    ) = "postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/postgres"
    READER_DB_URL: (
        str
    ) = "postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/postgres"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXPIRE_PERIOD: int = 3600
    JWT_REFRESH_TOKEN_EXPIRE_PERIOD: int = 3600
    SENTRY_SDN: str = ""
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_BACKEND_URL: (
        str
    ) = "db+postgresql://postgres:mysecretpassword@localhost:5432/postgres"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "audio"
    MINIO_SECURE: bool = False



class TestConfig(Config):
    ...


class LocalConfig(Config):
    ...


class ProductionConfig(Config):
    DEBUG: bool = False


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "test": TestConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
