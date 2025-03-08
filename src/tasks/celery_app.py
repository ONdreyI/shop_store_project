from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

from src.config import settings


celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=["src.tasks.celery_tasks"],  # Add your tasks here.
)

celery_instance.conf.beat_schedule = {
    "refresh-monthly-order-summary-every-hour": {
        "task": "src.tasks.celery_tasks.create_refresh_monthly_order_redis",
        "schedule": timedelta(seconds=300),
    },
}
