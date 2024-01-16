from datetime import timedelta
from celery import Celery

celery_app = Celery(__name__, broker=..., backend=...)
celery_app.autodiscover_tasks(["tasks"], force=True)
celery_app.conf.beat_schedule = {
    "publish_messages": {
        "task": "outbox.publish_messages",
        "schedule": timedelta(seconds=10),
    }
}
