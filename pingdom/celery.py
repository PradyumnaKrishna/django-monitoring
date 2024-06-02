from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pingdom.settings")

app = Celery("pingdom")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "check-websites-every-1-minute": {
        "task": "monitoring.tasks.check_website",
        "schedule": crontab(minute="*/1"),
        "args": (1,),  # Pass the website_id to the task
    },
}
