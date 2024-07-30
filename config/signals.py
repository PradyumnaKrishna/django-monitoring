# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from monitoring.models import Website
from celery.schedules import crontab
from config.celery import app
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json


@receiver(post_save, sender=Website)
def handle_new_website(sender, instance, created, **kwargs):
    if created:
        # Perform your activity here
        website_id = instance.id
        interval = 1  # Define your desired interval in minutes

        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=f"*/{interval}",
            hour="*",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        )

        task_name = f"check-website-{website_id}-every-{interval}-minute"

        PeriodicTask.objects.create(
            crontab=schedule,
            name=task_name,
            task="monitoring.tasks.check_website",
            args=json.dumps([website_id]),
        )
