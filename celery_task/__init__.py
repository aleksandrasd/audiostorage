from celery import Celery

from core.config import config

celery_app = Celery(
    "worker",
    backend=config.CELERY_BACKEND_URL,
    broker=config.CELERY_BROKER_URL,
)

# celery_app.conf.task_routes = {
#     "app.audio.input.celery_worker.audio.convert_audio": "q_convert_audio"
# }
celery_app.conf.update(task_track_started=True)
celery_app.autodiscover_tasks(["app.audio.adapter.input.celery.audio"])
