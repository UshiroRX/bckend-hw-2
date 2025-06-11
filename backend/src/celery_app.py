from celery import Celery
import os
from .config import settings
from celery.schedules import crontab

celery = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)
celery.conf.update(
    imports=("src.tasks.task"),
)

celery.conf.beat_schedule = { # fetch data every day once
     'fetch-data-daily': {
         'task': 'src.tasks.fetch_data_daily',
         'schedule': crontab(minute=0, hour=0),
     },
 }