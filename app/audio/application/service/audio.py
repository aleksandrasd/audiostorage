import asyncio
import os
from typing import List
from uuid import uuid4

from app.audio.adapter.output.persistence.repository_adapter import (
    AudioBinaryAdapterRepo,
    AudioRepositoryAdapter,
)
from app.audio.domain.command import ConvertAudioCommand, UploadAudioCommand
from app.audio.domain.entity.audio_file import (
    AudioFile,
    AudioFileRead,
    UserAudioFile,
    UserRawUploadedFile,
)
from app.audio.domain.usecase.audio import AudioServiceUseCase
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

    async def download_audio_file(self, filename: str, output_path: str) -> None:
        # TODO: throw exception
        await self.repo_binary.download_audio(
            name=filename, output_file_path=output_path
        )

    async def list_audio(self, user_id: int) -> List[AudioFileRead]:
        """Convert audio"""

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
        self, user_id: int | None = None, limit: int = 100
    ) -> List[AudioFileRead]:
        return await self.repository.list_audio_files(user_id, limit)

    async def files_full_text_search(
        self, user_id: int | None, limit: int = 100
    ) -> List[AudioFileRead]:
        return await self.repository.files_full_text_search(user_id, limit)

    @Transactional()
    async def convert_audio(self, command: ConvertAudioCommand) -> str:
        download_audio_formats = ["wav", "mp3"]
        file_name = await self.repository.get_raw_file_name(
            command.user_id
        )
        await self.repo_binary.download_audio(
            name=file_name, output_file_path=file_name
        )
        length_in_seconds = int(self.converter.get_audio_duration(file_name))
        generated_files = [file_name]
        try:
            for audio_format in download_audio_formats:
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
                    raw_audio_file_id=command.upload_id,
                )
                await self.repository.save_user_audio_file(user_audio)
                await self.repository.persist()
        finally:
            for fn in generated_files:
                os.remove(fn)
