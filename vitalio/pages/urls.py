# Django 
from django.urls import path

# Views 
from .views import home, about

urlpatterns = [
    path('', home, name="home"),
    path('about', about, name="about")
]