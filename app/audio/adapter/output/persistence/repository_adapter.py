import io
from typing import List

from app.audio.domain.entity.audio_file import (
    AudioFile,
    AudioFileMeta,
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

    def get_audio_upload_file_max_size(self) -> int | None:
        return self.audio_repo.get_audio_upload_file_max_size()

    def get_audio_formats_for_download(self) -> List[str] | None:
        return self.audio_repo.get_audio_formats_for_download()

    def get_max_audio_file_size(self) -> int:
        return self.audio_repo.get_max_audio_file_size()

    def save_upload_music_file_record(
        self, user_raw_uploaded_file: UserRawUploadedFile
    ) -> None:
        return self.audio_repo.get_max_audio_file_size()

    def save_audio_file_meta(self, audio_file_meta: AudioFileMeta) -> None:
        self.audio_repo.save_audio_file_meta(audio_file_meta)

    def save_audio_file(self, audio_file: AudioFile) -> None:
        self.audio_repo.save_audio_file(audio_file)

    def save_user_audio_file(self, user_audio_file: UserAudioFile) -> None:
        self.audio_repo.save_user_audio_file(user_audio_file)

    def persist(self) -> None:
        self.audio_repo.persist()

    def get_raw_audio_id(self, name: str) -> int:
        return self.audio_repo.get_raw_audio_id(name)


class ConvertedAudioAdapterRepo:
    def __init__(self, *, repo: ConvertedAudioRepo):
        self.repo = repo

    def get_task_status(self, task_id: str) -> TaskState:
        return self.repo.audio_res_repo.get_task_status(task_id)


class AudioBinaryAdapterRepo:
    def __init__(self, *, repo: AudioBinaryRepo):
        self.repo = repo

    def persist_raw_audio(self, name: str, data: io.BytesIO, length: int) -> None:
        self.repo.persist_raw_audio(name, data, length)

    def persist(self, name: str, file_path: str, audio_format: str) -> None:
        self.repo.persist(name, file_path, audio_format)

    def get_raw_audio(self, name: str, output_file_path: str) -> None:
        self.repo.get_raw_audio(name, output_file_path)
