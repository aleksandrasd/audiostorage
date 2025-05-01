import io
from abc import abstractmethod

from urllib3 import HTTPResponse


class AudioBinaryRepo:
    @abstractmethod
    def upload_audio(self, name: str, data: io.BytesIO, length: int) -> None:
        """Persist raw audio."""

    @abstractmethod
    def upload_audio_file(self, name: str, data: io.BytesIO, length: int) -> None:
        """Persist audio."""
    @abstractmethod
    async def remove_audio_file(self, name: str) -> None: 
        """Remove audio"""   

    @abstractmethod
    def download_audio(self, name: str, output_file_path: str) -> None:
        """Get raw audio."""

    @abstractmethod
    def get_audio(self, name) -> HTTPResponse:
        """Get audio."""
