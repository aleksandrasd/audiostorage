from abc import ABC, abstractmethod


class AudioMeta(ABC):
    @abstractmethod
    def get_audio_duration(self, file_path: str) -> float:
        """Get audio duration"""


class ConversionStrategy(ABC):
    @abstractmethod
    def convert(
        self, file_path: str, output_path: str, target_format: str, **kwargs
    ) -> None:
        """Convert audio into different format"""


class AudioConverter(AudioMeta, ConversionStrategy, ABC):
    def __init__(self, meta: AudioMeta, **conversions):
        self._meta = meta
        self.conversions = conversions

    def get_audio_duration(self, file_path: str) -> float:
        return self._meta.get_audio_duration(file_path)

    def convert(
        self, file_path: str, output_path: str, target_format: str, **kwargs
    ) -> None:
        strategy = self.conversions.get(target_format)
        if not strategy:
            raise ValueError(f"Unsupported target format: {target_format}")
        strategy.convert(file_path, output_path, **kwargs)
