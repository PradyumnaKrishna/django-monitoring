from django.shortcuts import render
from .models import Website, MonitoringResult


def website_list(request):
    websites = Website.objects.all()
    return render(request, "monitoring/index.html", {"websites": websites})


def monitoring_results(request, website_id):
    results = MonitoringResult.objects.filter(website_id=website_id).order_by(
        "-checked_at"
    )
    return render(request, "monitoring/monitoring_results.html", {"results": results})
