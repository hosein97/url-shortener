from celery import Celery
from celery.schedules import crontab
import os
from decouple import config as decouple_config

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    decouple_config("DJANGO_SETTINGS_MODULE", default="config.settings.development")
)

app = Celery("config")
# app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_url = decouple_config("CELERY_BROKER_URL")
app.conf.result_backend = decouple_config("CELERY_RESULT_BACKEND")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "flush-clicks": {
        "task": "shortener.tasks.flush_clicks_task",
        "schedule": 60.0,
    },
}