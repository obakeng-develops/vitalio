# Django
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.db import transaction

# Forms
from account.forms import ProfileForm

# Models 
from .models import Onboard
from account.models import Profile

def onboard_member(request):
    return render(request, "onboard/member/hello.html")

@transaction.atomic
def onboard_member_profile(request):

    if request.method == 'POST':

        form = ProfileForm(request.POST)

        if form.is_valid():
            # Change their isOnboarded value to true
            onboard = Onboard.objects.get(account=request.user)
            onboard.isOnboarded = True
            onboard.save()

            # Update their profile
            user = Profile.objects.get(account=request.user)
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()

            # Say thank you
            return redirect(reverse("member_dashboard"))
    else:

        form = ProfileForm()
        context = {
            "form": form
        }

    return render(request, "onboard/member/profile.html", context)

def onboard_admin(request):
    return render(request, "onboard/admin/hello.html")

def onboard_provider(request):
    return render(request, "onboard/provider/hello.html")

@transaction.atomic
def onboard_provider_profile(request):

    if request.method == 'POST':

        form = ProfileForm(request.POST)

        if form.is_valid():
            # Change their isOnboarded value to true
            onboard = Onboard.objects.get(account=request.user)
            onboard.isOnboarded = True
            onboard.save()

            # Update their profile
            user = Profile.objects.get(account=request.user)
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()

            # Say thank you
            return redirect(reverse("provider_dashboard"))
    else:

        form = ProfileForm()
        context = {
            "form": form
        }

    return render(request, "onboard/provider/profile.html", context)
