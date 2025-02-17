from celery import shared_task
from dependency_injector.wiring import Provide, inject

from app.audio.domain.command import ConvertAudioCommand
from app.audio.domain.usecase.audio import AudioServiceUseCase
from app.container import Container


@shared_task
@inject
def convert_audio(
    command: ConvertAudioCommand,
    service: AudioServiceUseCase = Provide[Container.audio_service],
) -> None:
    service.convert_audio(ConvertAudioCommand.model_validate(command))
