# app/audio/application/service/audio_service.py
import os

from celery import uuid

from app.audio.adapter.output.persistence.repository_adapter import (
    AudioBinaryAdapterRepo,
    AudioRepositoryAdapter,
)
from app.audio.application.exception import MissingPolicyException
from app.audio.domain.command import ConvertAudioCommand, UploadAudioCommand
from app.audio.domain.entity.audio_file import (
    AudioFile,
    AudioFileMeta,
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
        repo: AudioRepositoryAdapter,
        converter: AudioConverter,
        repo_binary: AudioBinaryAdapterRepo,
    ):
        self.repository = repo
        self.converter = converter
        self.repo_binary = repo_binary

    @Transactional()
    def upload_audio(self, command: UploadAudioCommand) -> str:
        new_name = str(uuid.uuid4())
        user_raw_uploaded_file = UserRawUploadedFile.create(
            user_id=command.user_id, file_name=new_name, original_file_name=command.name
        )
        self.repository.save_uploaded_audio_file(user_raw_uploaded_file)
        return new_name

    def _do_audio_file_conversion(self, file_name, audio_type) -> str:
        os.makedirs(audio_type, exist_ok=True)
        out_full_path = os.path.join(audio_type, file_name)
        try:
            self.converter.convert(file_name, out_full_path, audio_type)
        finally:
            if os.path.exists(out_full_path):
                os.remove(out_full_path)
        return out_full_path

    @Transactional()
    async def convert_audio(self, command: ConvertAudioCommand) -> str:
        file_name = command.file_name
        download_audio_formats = self.repository.get_audio_formats_for_download()
        if download_audio_formats is None:
            raise MissingPolicyException(
                (
                    "missing information what kind of audio "
                    "format to provide for users to download."
                )
            )
        self.repo_binary.get_raw_audio(name=file_name, output_file_path=file_name)
        length_in_seconds = int(self.converter.get_audio_duration(file_name))
        generated_files = []
        try:
            meta = AudioFileMeta.create(length_in_seconds=length_in_seconds)
            self.repository.save_audio_file_meta(meta)
            await self.repository.persist()

            for audio_format in command.audio_types:
                fmt_file_name = self._do_audio_file_conversion(file_name, audio_format)

                generated_files.append(fmt_file_name)

                self.repo_binary.persist(
                    name=file_name, file_path=fmt_file_name, audio_format=audio_format
                )

                audio_file = AudioFile.create(
                    meta_id=meta.id,
                    bucket=audio_format,
                    file_name=file_name,
                    file_type=audio_format,
                    file_size_in_bytes=os.path.getsize(file_name),
                )
                self.repository.save_audio_file(audio_file)
                self.repository.persist()

                # Link user and music_file
                user_audio = UserAudioFile.create(
                    user_id=command.user_Id,
                    audio_file_id=audio_file.id,
                    raw_audio_file_id=self.repository.get_upload_id_by_file_name(
                        file_name
                    ),
                )
                self.repository.save_user_audio_file(user_audio)
                self.repository.persist()
        finally:
            for fn in generated_files:
                os.remove(fn)
