from django.db import models


class Website(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MonitoringResult(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    status_code = models.IntegerField()
    response_time = models.FloatField()
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.website.name} - {self.status_code} - {self.response_time}s"
