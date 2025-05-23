from abc import ABC, abstractmethod
from typing import List

from app.audio.domain.entity.audio_file import (
    AudioFile,
    AudioFileRead,
    UserAudioFile,
    UserRawUploadedFile,
)


class AudioRepo(ABC):
    @abstractmethod
    async def get_file_extension_by_id(self, id: str) -> str:
        """get file extension by id"""

    @abstractmethod
    async def get_original_file_name_by_id(self, id: str) -> str | None:
        """get original file name by id"""
    
    @abstractmethod
    async def get_file_name_by_id(self, id: str) -> str:
        """get file name by id"""
      
    @abstractmethod
    async def save_upload_audio_file_record(
        self, user_raw_uploaded_file: UserRawUploadedFile
    ) -> None:
        """save_upload_music_file_record"""

    @abstractmethod
    async def save_audio_file(self, audio_file: AudioFile) -> None:
        """save_audio_file"""

    @abstractmethod
    async def save_user_audio_file(self, user_audio_file: UserAudioFile) -> None:
        """save_audio_file"""

    @abstractmethod
    async def persist(self) -> None:
        """persist"""

    @abstractmethod
    async def get_audio_upload_file_max_size(self) -> int | None:
        """get_audio_upload_file_max_size"""

    @abstractmethod
    async def get_audio_formats_for_download(self) -> List[str] | None:
        """get_audio_formats_for_download"""

    @abstractmethod
    async def download_audio_id(self, name: str) -> int:
        """download_audio_id"""

    @abstractmethod
    async def search_audio_files(self, query: str, user_id: int | None, limit: int, offset: int) -> tuple[list[AudioFileRead], int]:
        """search_audio_files"""

    @abstractmethod
    async def list_audio_files(
        self, user_id: int | None, limit: int, offset: int
    ) -> tuple[list[AudioFileRead], int]:
        """list_audio_files"""

    @abstractmethod
    async def list_user_audio_files(
        self, nickname: str | None = None, page: int = 1, per_page = 10
    ) -> tuple[list[AudioFileRead], int]:
        """list_user_audio_files"""
        

    @abstractmethod
    async def get_upload_file_name(self, id: int) -> str | None:
        """Get raw file name"""
    @abstractmethod
    async def get_user_upload_file_name(self, id: int, user_id: int) -> str | None:
        """Get raw file name"""    

    @abstractmethod
    async def remove_audio_file(self, audio_file_id: str) -> None:
        """Remove audio file"""