from abc import abstractmethod
from typing import List

from app.audio.domain.command import ConvertAudioCommand, RemoveAudioCommand, UploadAudioCommand
from app.audio.domain.entity.audio_file import AudioFileCountedRead, AudioFileRead


class AudioServiceUseCase:
    @abstractmethod
    async def get_download_file_name(self, id: str) -> str:
        """Get download file name by id"""

    @abstractmethod
    async def download_audio_file(self, filename: str, output_path: str) -> None:
        """download_audio_file"""

    @abstractmethod
    async def get_file_name_by_id(self, id: str) -> None:
        """download_audio_file"""

    @abstractmethod
    async def upload_audio(self, command: UploadAudioCommand) -> str:
        """Upload audio file"""

    @abstractmethod
    async def remove_audio_file(self, command: RemoveAudioCommand) -> None:
        """Remove audio file"""

    @abstractmethod
    async def convert_audio(self, command: ConvertAudioCommand) -> str:
        """Convert audio file"""
        

    @abstractmethod
    async def search_audio_files(
        self, user_id: int | None, page: int, per_page = 20
    ) -> AudioFileCountedRead:
        """search_audio_files"""

    @abstractmethod
    async def list_audio_files(
        self, user_id: int | None = None, page: int = 1, per_page = 10
    ) -> AudioFileCountedRead:
        """List audio file collection"""

    @abstractmethod
    async def list_user_audio_files(
        self, nickname: str | None = None, page: int = 1, per_page = 10
    ) -> AudioFileCountedRead:
        """List user's audio file collection"""

    @abstractmethod
    async def remove_file(command: RemoveAudioCommand) -> None:
        """Remove audio file"""
