from abc import ABC, abstractmethod
from typing import Mapping


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
    def __init__(
        self, meta: AudioMeta, conversion_strategies: Mapping[str, ConversionStrategy]
    ):
        self._meta = meta
        self._conversion_strategies = conversion_strategies

    def get_audio_duration(self, file_path: str) -> float:
        return self._meta(file_path)

    def convert(
        self, file_path: str, output_path: str, target_format: str, **kwargs
    ) -> None:
        strategy = self._conversion_strategies.get(target_format)
        if not strategy:
            raise ValueError(f"Unsupported target format: {target_format}")
        strategy.convert(file_path, output_path, **kwargs)
