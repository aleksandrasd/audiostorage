from abc import ABC, abstractmethod

from core.celery import TaskState


class ConvertedAudioRepo(ABC):
    @abstractmethod
    def get_task_status(self, task_id: str) -> TaskState:
        """Get task status"""
