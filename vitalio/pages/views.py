# Django
from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html")

def about(request):
    return render(request, "pages/about.html")

def pricing(request):
    return render(request, "pages/pricing.html")

def demo(request):
    return render(request, "pages/demo.html")

def business(request):
    return render(request, "pages/business.html")

def patients(request):
    return render(request, "pages/patients.html")