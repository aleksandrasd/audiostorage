from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.audio.adapter.output.persistence.repository_adapter import (
    AudioBinaryAdapterRepo,
    AudioRepositoryAdapter,
)
from app.audio.application.service.audio import AudioService
from app.auth.application.service.jwt import JwtService
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.application.service.user import UserService
from core.audio_editor import AudioConverter
from core.audio_editor.backend.ffmpeg import (
    FFmpegAudioMeta,
    FFmpegMP3Conversion,
    FFmpegWAVConversion,
)


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    user_repo = Singleton(UserSQLAlchemyRepo)
    user_repo_adapter = Factory(UserRepositoryAdapter, user_repo=user_repo)
    user_service = Factory(UserService, repository=user_repo_adapter)

    jwt_service = Factory(JwtService)

    ffmpeg_audio_meta = Singleton(FFmpegAudioMeta)
    ffmpeg_wav_conversion = Singleton(FFmpegWAVConversion)
    ffmpeg_mp3_conversion = Singleton(FFmpegMP3Conversion)

    audio_converter = Factory(
        AudioConverter,
        ffmpeg_audio_meta=ffmpeg_audio_meta,
        conversion_dict={"wav": ffmpeg_wav_conversion, "mp3": ffmpeg_mp3_conversion},
    )
    audio_repo = (Singleton(),)
    audio_repo_adapter = Factory(AudioRepositoryAdapter)
    audio_binary_repo_adapter = Singleton(AudioBinaryAdapterRepo)

    audio_service = Factory(
        AudioService,
        repo=audio_repo_adapter,
        converter=audio_converter,
        repo_binary=audio_binary_repo_adapter,
    )
