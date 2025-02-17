import io

import urllib3

from app.audio.domain.repository.audiobinary import AudioBinaryRepo
from minio_storage import minio_client


class AudioBinaryMinioRepo(AudioBinaryRepo):
    def persist_raw_audio(self, name: str, data: io.BytesIO, length: int) -> None:
        minio_client.put_object(
            bucket_name="raw", object_name=name, data=data, length=length
        )

    def persist(self, name: str, file_path: str, audio_format: str) -> None:
        minio_client.fput_object(
            bucket_name=audio_format, object_name=name, file_path=file_path
        )

    def get_raw_audio(self, name: str, output_file_path: str) -> None:
        minio_client.fget_object("raw", name, output_file_path)

    def get_audio(self, name, audio_type) -> urllib3.response.HTTPResponse:
        return minio_client.get_object(bucket_name=audio_type, object_name=name)
