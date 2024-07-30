from django.urls import path
from . import views

urlpatterns = [
    path("", views.website_list, name="website_list"),
    path(
        "sites/<int:website_id>/", views.monitoring_results, name="monitoring_results"
    ),
]
