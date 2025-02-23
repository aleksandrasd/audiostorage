# from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
# from dependency_injector.providers import Factory, Singleton

# from app.audio.adapter.output.persistence.minio.audio import AudioBinaryMinioRepo
# from app.audio.adapter.output.persistence.repository_adapter import (
#     AudioBinaryAdapterRepo,
#     AudioRepositoryAdapter,
# )
# from app.audio.adapter.output.persistence.sqlalchemy.audio import AudioSQLAlchemyRepo
# from app.audio.application.service.audio import AudioService
# from core.audio_editor import AudioConverter
# from core.audio_editor.backend.ffmpeg import (
#     FFmpegAudioMeta,
#     FFmpegMP3Conversion,
#     FFmpegWAVConversion,
# )


# class AudioContainer(DeclarativeContainer):
#     wiring_config = WiringConfiguration(packages=["app.audio.adapter.input.celery"])

#     ffmpeg_audio_meta = Singleton(FFmpegAudioMeta)
#     ffmpeg_wav_conversion = Singleton(FFmpegWAVConversion)
#     ffmpeg_mp3_conversion = Singleton(FFmpegMP3Conversion)

#     audio_converter = Factory(
#         AudioConverter,
#         meta=ffmpeg_audio_meta,
#         conversions={
#             'wav': ffmpeg_wav_conversion,
#             'mp3': ffmpeg_mp3_conversion
#         }
#     )
#     audio_repo = Singleton(AudioSQLAlchemyRepo)
#     audio_repo_adapter = Factory(AudioRepositoryAdapter,audio_repo = audio_repo)
#     audio_binary_repo = Singleton(AudioBinaryMinioRepo)
#     audio_binary_repo_adapter = Factory(AudioBinaryAdapterRepo,repo = audio_binary_repo)

#     audio_service = Factory(
#       AudioService,
#       repository = audio_repo_adapter,
#       converter = audio_converter,
#       repo_binary = audio_binary_repo_adapter
#     )
