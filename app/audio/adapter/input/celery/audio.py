import asyncio

from celery import shared_task
from dependency_injector.wiring import Provide, inject

from app.audio.domain.command import ConvertAudioCommand
from app.audio.domain.usecase.audio import AudioServiceUseCase
from app.container import Container
from celery_task.name import CONVERT_AUDIO
from core.db.session import FunScopedSession


@FunScopedSession()
@inject
async def _convert_audio(
    user_id: int,
    file_name: str,
    usecase: AudioServiceUseCase = Provide[Container.audio_service],
) -> None:
    command = ConvertAudioCommand(user_id=user_id, file_name=file_name)
    await usecase.convert_audio(command)


@shared_task(name=CONVERT_AUDIO)
def convert_audio(user_id: int, upload_id: int):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
        _convert_audio(user_id=user_id, upload_id=upload_id)
    )
    return result


audio_container = Container()
