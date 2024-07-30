from django.shortcuts import render
from .models import Website, MonitoringResult
from django.contrib.auth.decorators import login_required


@login_required
def website_list(request):
    # Get user websites
    websites = Website.objects.filter(owner=request.user)

    return render(request, "monitoring/index.html", {"websites": websites})


@login_required
def monitoring_results(request, website_id):
    website = Website.objects.filter(id=website_id).first()

    # Check if the website exists and belongs to the user
    if not website or (website and website.owner != request.user):
        # return not found
        return render(request, "404.html", status=404)

    results = MonitoringResult.objects.filter(website=website).order_by(
        "-checked_at"
    )
    return render(request, "monitoring/monitoring_results.html", {"website": website, "results": results})
