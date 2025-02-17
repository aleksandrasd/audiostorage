import io
from abc import abstractmethod

import urllib3


class AudioBinaryRepo:
    @abstractmethod
    def persist_raw_audio(self, name: str, data: io.BytesIO, length: int) -> None:
        """Persist raw audio."""

    @abstractmethod
    def persist(
        self, name: str, data: io.BytesIO, length: int, audio_format: str
    ) -> None:
        """Persist audio."""

    @abstractmethod
    def get_raw_audio(self, name: str, output_file_path: str) -> None:
        """Get raw audio."""

    @abstractmethod
    def get_audio(self, name, audio_type) -> urllib3.response.HTTPResponse:
        """Get audio."""
