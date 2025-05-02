import io
from typing import List

from urllib3 import HTTPResponse

from app.audio.domain.entity.audio_file import (
    AudioFile,
    AudioFileCountedRead,
    AudioFileRead,
    UserAudioFile,
    UserRawUploadedFile,
)
from app.audio.domain.repository.audio import AudioRepo
from app.audio.domain.repository.audiobinary import AudioBinaryRepo
from app.user.domain.repository.converted_audio import ConvertedAudioRepo
from core.celery import TaskState


class AudioRepositoryAdapter:
    def __init__(self, *, audio_repo: AudioRepo):
        self.audio_repo = audio_repo

    async def get_file_name_by_id(self, id: str) -> None:
        return await self.audio_repo.get_file_name_by_id(id)
    
    async def get_original_file_name_by_id(self, id: str) -> str | None:
        return await self.audio_repo.get_original_file_name_by_id(id)
    
    async def get_file_extension_by_id(self, id: str) -> None:
        return await self.audio_repo.get_file_extension_by_id(id)
    
    async def get_upload_file_name(self, id: int) -> str:
        return await self.audio_repo.get_upload_file_name(
            id
        )
    
    async def get_user_upload_file_name(self, id: int, user_id: int) -> str | None:
        return await self.audio_repo.get_user_upload_file_name(
            id, user_id
        )     

      
    async def save_upload_audio_file_record(
        self, user_raw_uploaded_file: UserRawUploadedFile
    ) -> None:
        await self.audio_repo.save_upload_audio_file_record(
            user_raw_uploaded_file
        )

    async def get_audio_upload_file_max_size(self) -> int | None:
        return await self.audio_repo.get_audio_upload_file_max_size()

    async def get_audio_formats_for_download(self) -> List[str] | None:
        return await self.audio_repo.get_audio_formats_for_download()

    async def save_audio_file(self, audio_file: AudioFile) -> None:
        await self.audio_repo.save_audio_file(audio_file)

    async def save_user_audio_file(self, user_audio_file: UserAudioFile) -> None:
        await self.audio_repo.save_user_audio_file(user_audio_file)

    async def persist(self) -> None:
        await self.audio_repo.persist()

    async def download_audio_id(self, name: str) -> int:
        return await self.audio_repo.download_audio_id(name)

    async def get_bucket_by_filename(
        self, filename: str, original_file_name: str
    ) -> str | None:
        return await self.audio_repo.get_bucket_by_filename(
            filename=filename, original_file_name=original_file_name
        )

    async def list_audio_files(
        self, user_id: int | None, limit, offset
    ) -> AudioFileCountedRead:
        audio_files, total_records = await self.audio_repo.list_audio_files(user_id, limit=limit, offset=offset)  
        audio_file_reads = [AudioFileRead.model_validate(audio_file) for audio_file in audio_files]
        return AudioFileCountedRead(data=audio_file_reads, total_records = total_records, limit=limit, offset=offset)
    
    async def list_user_audio_files(
        self, nickname: str, limit, offset
    ) -> AudioFileCountedRead:
        audio_files, total_records = await self.audio_repo.list_user_audio_files(nickname, limit=limit, offset=offset)  
        audio_file_reads = [AudioFileRead.model_validate(audio_file) for audio_file in audio_files]
        return AudioFileCountedRead(data=audio_file_reads, total_records = total_records, limit=limit, offset=offset)


    async def search_audio_files(
        self, query: str, user_id: int | None, limit: int, offset: int
    ) -> AudioFileCountedRead:
        audio_files, total_records  = await self.audio_repo.search_audio_files(query, user_id, limit = limit, offset=offset)
        audio_file_reads = [AudioFileRead.model_validate(audio_file) for audio_file in audio_files]
        return AudioFileCountedRead(data=audio_file_reads, total_records = total_records, limit=limit, offset=offset)


class AudioBinaryAdapterRepo:
    def __init__(self, *, repo: AudioBinaryRepo):
        self.repo = repo

    async def upload_audio(self, name: str, data: io.BytesIO, length: int) -> None:
        await self.repo.upload_audio(name, data, length)

    async def upload_audio_file(
        self, name: str, file_path: str
    ) -> None:
        await self.repo.upload_audio_file(name, file_path)

    async def download_audio(self, name: str, output_file_path: str) -> None:
        await self.repo.download_audio(name, output_file_path)

    async def get_audio(self, name) -> HTTPResponse:
        await self.repo.get_audio(name)

    async def remove_audio_file(self, name: str) -> None:
        await self.repo.remove_audio_file(name)
