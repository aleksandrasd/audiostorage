from abc import abstractmethod

from app.audio.domain.command import ConvertAudioCommand, UploadAudioCommand


class AudioServiceUseCase:
    @abstractmethod
    def upload_audio(self, command: UploadAudioCommand) -> str:
        """Upload audio"""

    @abstractmethod
    def convert_audio(self, command: ConvertAudioCommand) -> str:
        """Convert audio"""
