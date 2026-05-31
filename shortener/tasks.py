from celery import shared_task
from .services import flush_clicks

@shared_task
def flush_clicks_task():
    flush_clicks()