import asyncio
import os
from typing import List
from uuid import uuid4

from app.audio.adapter.output.persistence.exception import FileRemoveError
from app.audio.adapter.output.persistence.repository_adapter import (
    AudioBinaryAdapterRepo,
    AudioRepositoryAdapter,
)
from app.audio.application.exception import AudioFileNotFound
from app.audio.domain.command import ConvertAudioCommand, RemoveAudioCommand, UploadAudioCommand
from app.audio.domain.entity.audio_file import (
    AudioFile,
    AudioFileCountedRead,
    AudioFileRead,
    UserAudioFile,
    UserRawUploadedFile,
)
from app.audio.domain.usecase.audio import AudioServiceUseCase
from core.config import config
from core.audio_editor import AudioConverter
from core.db.transactional import Transactional


class AudioService(AudioServiceUseCase):
    def __init__(
        self,
        *,
        repository: AudioRepositoryAdapter,
        converter: AudioConverter,
        repo_binary: AudioBinaryAdapterRepo,
    ):
        self.repository = repository
        self.converter = converter
        self.repo_binary = repo_binary
    
    async def get_download_file_name(self, id: str) -> str | None:
        original_file_name  = await self.repository.get_original_file_name_by_id(id)
        if not original_file_name:
            return None
        ext = await self.repository.get_file_extension_by_id(id)
        base_name, _ = os.path.splitext(original_file_name)
        return f"{base_name}.{ext}"
    
    async def download_audio_file(self, id: str, output_path: str) -> None:
        file_name = await self.repository.get_file_name_by_id(id)
        await self.repo_binary.download_audio(
            name=file_name, output_file_path=output_path
        )

    @Transactional()
    async def remove_audio_file(self, command: RemoveAudioCommand) -> None:
        audio_file_id = command.uploaded_audio_file_id
        user_id = command.user_id
        file_name = await self.repository.get_user_upload_file_name(audio_file_id, user_id)
        if not file_name:
          raise AudioFileNotFound
        await self.repository.remove_audio_file(audio_file_id)
        try:
          await self.repo_binary.remove_audio_file(file_name)
        except FileRemoveError as e:
            pass

    @Transactional()
    async def upload_audio(self, command: UploadAudioCommand) -> int:
        upload_name = str(uuid4())
        await self.repo_binary.upload_audio(
            name=upload_name, data=command.data, length=command.len
        )
        user_raw_uploaded_file = UserRawUploadedFile.create(
            file_name=upload_name,
            original_file_name=command.name,
        )
        await self.repository.save_upload_audio_file_record(user_raw_uploaded_file)
        await self.repository.persist()
        return user_raw_uploaded_file.id

    def _do_audio_file_conversion(self, file_name, audio_type) -> str:
        os.makedirs(audio_type, exist_ok=True)
        out_full_path = os.path.join(audio_type, str(uuid4()))
        self.converter.convert(file_name, out_full_path, audio_type)
        return out_full_path

    async def list_audio_files(
        self, user_id: int | None, page: int, per_page = 20
    ) -> AudioFileCountedRead:
        if per_page > 20:
            per_page = 20
        return await self.repository.list_audio_files(user_id, limit=per_page,  offset=per_page * (page-1))
    
    async def list_user_audio_files(
        self, nickname: str, page: int = 1, per_page = 10
    ) -> AudioFileCountedRead:
        if per_page > 20:
            per_page = 20
        return await self.repository.list_user_audio_files(nickname, limit=per_page,  offset=per_page * (page-1))
        
  
    async def search_audio_files(
        self, query: str, user_id: int | None, page: int, per_page = 20
    ) -> AudioFileCountedRead:
        if per_page > 20:
            per_page = 20
        return await self.repository.search_audio_files(query, user_id, limit = per_page, offset = per_page * (page-1))

    @Transactional()
    async def convert_audio(self, command: ConvertAudioCommand) -> str:
        file_name = await self.repository.get_upload_file_name(
            command.upload_id
        )
        await self.repo_binary.download_audio(
            name=file_name, output_file_path=file_name
        )
        length_in_seconds = int(self.converter.get_audio_duration(file_name))
        generated_files = [file_name]
        try:
            for audio_format in config.AUDIO_FORMATS:
                fmt_file_name = await asyncio.to_thread(
                    self._do_audio_file_conversion,
                    file_name=file_name,
                    audio_type=audio_format,
                )
                generated_files.append(fmt_file_name)
                await self.repo_binary.upload_audio_file(
                    name=os.path.basename(fmt_file_name), 
                    file_path=fmt_file_name
                )

                audio_file = AudioFile.create(
                    length_in_seconds=length_in_seconds,
                    file_name=os.path.basename(fmt_file_name),
                    file_type=audio_format,
                    file_size_in_bytes=os.path.getsize(fmt_file_name),
                )
                await self.repository.save_audio_file(audio_file)
                await self.repository.persist()

                user_audio = UserAudioFile.create(
                    user_id=command.user_id,
                    audio_file_id=str(audio_file.id),
                    upload_id=command.upload_id,
                )
                await self.repository.save_user_audio_file(user_audio)
                await self.repository.persist()
        finally:
            for fn in generated_files:
                os.remove(fn)
