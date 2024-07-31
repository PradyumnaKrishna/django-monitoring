import requests

from .models import Website, MonitoringResult
from django.core.mail import send_mail
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def check_website(website_id):
    logger.info(f"Sending request for website_id {website_id}")
    website = Website.objects.get(id=website_id)
    try:
        response = requests.get(website.url)
        status_code = response.status_code
        response_time = response.elapsed.total_seconds()*1000
    except requests.RequestException:
        status_code = 0
        response_time = 0

    result = MonitoringResult.objects.create(
        website=website,
        status_code=status_code,
        response_time=response_time,
    )

    if not result.is_up():
        if website.alert:
            email_alert.delay(website_id)
        if website.webhook:
            call_webhook.delay(website.webhook)


@shared_task
def call_webhook(url: str):
    requests.get(url)


@shared_task
def email_alert(website_id):
    website = Website.objects.get(id=website_id)
    owner = website.owner

    last_result = (
        MonitoringResult.objects.filter(website=website).order_by("-checked_at").first()
    )

    if last_result and not last_result.is_up() and owner.email:
        send_mail(
            "Website Down",
            f"The website {website.name} is down. Status code: {last_result.status_code}",
            "admin@dj-monitor.com",
            [owner.email],
            fail_silently=False,
        )
