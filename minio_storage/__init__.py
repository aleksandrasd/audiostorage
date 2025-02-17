from minio import Minio

from core.config import get_config

minio_client = Minio(
    get_config().MINIO_ENDPOINT,
    access_key=get_config().MINIO_ACCESS_KEY,
    secret_key=get_config().MINIO_SECRET_KEY,
    secure=get_config().MINIO_SECURE,
)
