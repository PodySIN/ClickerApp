import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("users")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "daily-midnight-moscow": {
        "task": "users.tasks.daily_refresh",
        "schedule": crontab(hour=0, minute=0),  ##crontab(hour=21, minute=0)
        "args": (),
    },
}
