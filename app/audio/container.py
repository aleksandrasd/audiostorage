from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.audio.adapter.output.persistence.repository_adapter import (
    AudioBinaryAdapterRepo,
    AudioRepositoryAdapter,
)
from app.audio.application.service.audio import AudioService
from core.audio_editor import AudioConverter
from core.audio_editor.backend.ffmpeg import (
    FFmpegAudioMeta,
    FFmpegMP3Conversion,
    FFmpegWAVConversion,
)


class AudioContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app"])

    ffmpeg_audio_meta = Singleton(FFmpegAudioMeta)
    ffmpeg_wav_conversion = Singleton(FFmpegWAVConversion)
    ffmpeg_mp3_conversion = Singleton(FFmpegMP3Conversion)

    audio_converter = Factory(
        AudioConverter,
        ffmpeg_audio_meta=ffmpeg_audio_meta,
        conversion_dict={"wav": ffmpeg_wav_conversion, "mp3": ffmpeg_mp3_conversion},
    )
    audio_repository_adapter = Factory(AudioRepositoryAdapter)
    audio_binary_repo = Singleton(AudioBinaryAdapterRepo)

    audio_service = Factory(
        AudioService,
        repo=audio_repository_adapter,
        converter=audio_converter,
        repo_binary=audio_binary_repo,
    )
