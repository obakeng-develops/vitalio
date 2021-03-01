# Django
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.db import transaction

# Forms
from account.forms import ProfileForm
from company.forms import CompanyForm

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

@transaction.atomic
def onboard_admin_profile(request):

    if request.method == 'POST':

        form = ProfileForm(request.POST)

        if form.is_valid():

            # Update their profile
            user = Profile.objects.get(account=request.user)
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()

            # Say thank you
            return redirect(reverse("onboard_admin_company"))
    else:

        form = ProfileForm()
        context = {
            "form": form
        }

    return render(request, "onboard/admin/profile.html")

@transaction.atomic
def onboard_admin_company(request):

    if request.method == 'POST':

        form = CompanyForm(request.POST)

        if form.is_valid():
            # Change their isOnboarded value to true
            onboard = Onboard.objects.get(account=request.user)
            onboard.isOnboarded = True
            onboard.save()

            # Update their profile
            company = CompanyForm()
            company.company_name = form.cleaned_data["company_name"]
            company.company_size = form.cleaned_data["company_size"]
            company.save()

            # Say thank you
            return redirect(reverse("member_dashboard"))
    else:

        form = CompanyForm()
        context = {
            "form": form
        }


    return render(request, "onboard/admin/company.html")

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
