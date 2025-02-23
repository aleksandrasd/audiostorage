# import asyncio


# from app.user.domain.repository.converted_audio import ConvertedAudioRepo
# from celery_task import celery_app
# from core.celery import TaskState
# from celery.result import AsyncResult


# class ConvertedAudioCeleryRepo(ConvertedAudioRepo):
#     async def get_task_status(self, task_id: str) -> TaskState:
#         result = asyncio.to_thread(AsyncResult, id = task_id, app=celery_app)
#         return result.status
