from abc import ABC, abstractmethod
from typing import List

from app.audio.domain.entity.audio_file import (
    AudioFile,
    AudioFileMeta,
    UserAudioFile,
    UserRawUploadedFile,
)


class AudioRepo(ABC):
    @abstractmethod
    def save_upload_music_file_record(
        self, user_raw_uploaded_file: UserRawUploadedFile
    ) -> None:
        """save_upload_music_file_record"""

    @abstractmethod
    def save_audio_file_meta(self, audio_file_meta: AudioFileMeta) -> None:
        """save_audio_file_meta"""

    @abstractmethod
    def save_audio_file(self, audio_file: AudioFile) -> None:
        """save_audio_file"""

    @abstractmethod
    def save_user_audio_file(self, user_audio_file: UserAudioFile) -> None:
        """save_audio_file"""

    @abstractmethod
    def persist(self) -> None:
        """persist"""

    @abstractmethod
    def get_audio_upload_file_max_size(self) -> int | None:
        """get_audio_upload_file_max_size"""

    @abstractmethod
    def get_audio_formats_for_download(self) -> List[str] | None:
        """get_audio_formats_for_download"""

    @abstractmethod
    def get_raw_audio_id(name: str) -> int:
        """get_raw_audio_id"""
