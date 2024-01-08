import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "weekly_posts": {
        "task": "news.tasks.weekly_posts",
        "schedule": crontab(hour='08', minute='00', day_of_week='mon'),
    }
}

app.autodiscover_tasks()
