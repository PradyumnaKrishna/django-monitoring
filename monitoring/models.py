from django.db import models


# Model to store website for monitoring.
class Website(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    webhook = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    alert = models.BooleanField(default=False)
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    # Website last online time.
    def last_online(self):
        return self.results.filter(status_code__lt=400).order_by("-checked_at").first().checked_at

    def __str__(self):
        return self.name


class MonitoringResult(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="results")
    status_code = models.IntegerField()
    response_time = models.FloatField()
    checked_at = models.DateTimeField(auto_now_add=True)

    # Is the website up?
    def is_up(self):
        return self.status_code < 400

    def __str__(self):
        return f"{self.website.name} - {self.status_code} - {self.response_time}s"
