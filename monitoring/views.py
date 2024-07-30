from django.shortcuts import render, redirect, resolve_url
from .models import Website, MonitoringResult
from django.contrib.auth.decorators import login_required


@login_required
def website_list(request):
    # Get user websites
    websites = Website.objects.filter(owner=request.user)

    return render(request, "monitoring/index.html", {"websites": websites, "user": request.user})


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


@login_required
def add_website(request):
    # Check if the request is POST
    if request.method == "POST":

        # Get the form data
        name = request.POST.get("name")
        url = request.POST.get("url")
        alert = request.POST.get("alert") == 'on'
        webhook = request.POST.get("webhook")

        # Create the website alert
        website = Website.objects.create(
            name=name, url=url, owner=request.user, alert=alert, webhook=webhook
        )

        # Redirect to the results page
        return redirect(resolve_url("results", website_id=website.id))

    return redirect("")
