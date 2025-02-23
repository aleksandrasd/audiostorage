from abc import abstractmethod
from typing import List

from app.audio.domain.command import ConvertAudioCommand, UploadAudioCommand
from app.audio.domain.entity.audio_file import AudioFileRead


class AudioServiceUseCase:
    @abstractmethod
    async def download_audio_file(self, filename: str, output_path: str) -> None:
        """download_audio_file"""

    @abstractmethod
    async def upload_audio(self, command: UploadAudioCommand) -> str:
        """Upload audio"""

    @abstractmethod
    async def convert_audio(self, command: ConvertAudioCommand) -> str:
        """Convert audio"""

    @abstractmethod
    async def list_audio(self, user_id: int) -> List[AudioFileRead]:
        """Convert audio"""

    @abstractmethod
    async def files_full_text_search(
        self, query: str, limit: int = 100
    ) -> List[AudioFileRead]:
        """files_full_text_search"""

    @abstractmethod
    async def list_audio_files(
        self, user_id: int | None = None, limit: int = 100
    ) -> List[AudioFileRead]:
        """list_audio_files"""
