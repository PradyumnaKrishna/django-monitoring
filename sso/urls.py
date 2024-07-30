from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login/github/', views.github_login, name='github_login'),
    path('login/callback/', views.github_callback, name='github_callback'),
]
