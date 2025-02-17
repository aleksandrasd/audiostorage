from multiprocessing.pool import AsyncResult

from app.user.domain.repository.converted_audio import ConvertedAudioRepo
from celery_task import celery_app
from core.celery import TaskState


class ConvertedAudioCeleryRepo(ConvertedAudioRepo):
    def get_task_status(self, task_id: str) -> TaskState:
        return AsyncResult(task_id, app=celery_app).status
