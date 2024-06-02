# from pingdom.celery import shared_task
import requests
from .models import Website, MonitoringResult
from django.core.mail import send_mail
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def check_website(website_id):
    website = Website.objects.get(id=website_id)
    try:
        response = requests.get(website.url)
        status_code = response.status_code
        response_time = response.elapsed.total_seconds()
    except requests.RequestException:
        status_code = 0
        response_time = 0.0

    MonitoringResult.objects.create(
        website=website,
        status_code=status_code,
        response_time=response_time,
    )

    if status_code != 200:
        notify_downtime.delay(website_id)


@shared_task
def notify_downtime(website_id):
    website = Website.objects.get(id=website_id)
    last_result = (
        MonitoringResult.objects.filter(website=website).order_by("-checked_at").first()
    )
    if last_result and last_result.status_code != 200:
        send_mail(
            "Website Down",
            f"The website {website.name} is down. Status code: {last_result.status_code}",
            "from@example.com",
            ["user@example.com"],
            fail_silently=False,
        )
