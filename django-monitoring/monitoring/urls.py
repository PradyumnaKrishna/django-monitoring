from django.urls import path
from . import views

urlpatterns = [
    path("", views.website_list, name="websites"),
    path(
        "sites/<int:website_id>/", views.monitoring_results, name="results"
    ),
    path("add/", views.add_website, name="add_website"),
]
