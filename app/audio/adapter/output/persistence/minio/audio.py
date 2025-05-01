import asyncio
import io

import urllib3
from minio.deleteobjects import DeleteObject
from app.audio.adapter.output.persistence.exception import FileRemoveError
from app.audio.domain.repository.audiobinary import AudioBinaryRepo
from core.config import config
from minio_storage import minio_client


class AudioBinaryMinioRepo(AudioBinaryRepo):
    async def upload_audio(self, name: str, data: io.BytesIO, length: int) -> None:
        await asyncio.to_thread(
            minio_client.put_object,
            bucket_name=config.BUCKET_NAME,
            object_name=name,
            data=data,
            length=length,
        )

    async def upload_audio_file(self, name: str, file_path: str) -> None:
        await asyncio.to_thread(
            minio_client.fput_object,
            bucket_name=config.BUCKET_NAME,
            object_name=name,
            file_path=file_path,
        )
       
    async def download_audio(self, name: str, output_file_path: str) -> None:
        await asyncio.to_thread(
            minio_client.fget_object, config.BUCKET_NAME, name, output_file_path
        )

    async def remove_audio_file(self, name: str) -> None:
      errors = await asyncio.to_thread(minio_client.remove_objects(
          config.BUCKET_NAME,
          [
              DeleteObject(object_name=name)
          ]
      ))
      if len(errors) > 0:
        raise FileRemoveError(errors)

    async def get_audio(self, name: str) -> urllib3.HTTPResponse:
        return await asyncio.to_thread(
            minio_client.get_object,
            bucket_name=config.BUCKET_NAME,
            object_name=name,
        )
