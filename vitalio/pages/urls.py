# Django 
from django.urls import path

# Views 
from .views import home, about, pricing

urlpatterns = [
    path('', home, name="home"),
    path('about', about, name="about"),
    path('pricing', pricing, name="pricing")
]