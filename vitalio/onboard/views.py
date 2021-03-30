# Django
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.db import transaction

# Forms
from account.forms import ProfileForm
from company.forms import CompanyForm
from provider.forms import ProviderForm

# Models 
from .models import Onboard
from account.models import Profile
from company.models import Company, AccountCompany
from provider.models import Provider

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

    return render(request, "onboard/admin/profile.html", context)

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
            company = Company()
            company.company_name = form.cleaned_data["company_name"]
            company.company_size = form.cleaned_data["company_size"]
            company.save()

            # Add user as part of a company
            account_company = AccountCompany()
            account_company.company = company
            account_company.user = request.user
            account_company.save()

            # Say thank you
            return redirect(reverse("member_dashboard"))
    else:

        form = CompanyForm()
        context = {
            "form": form
        }


    return render(request, "onboard/admin/company.html", context)

def onboard_provider(request):

    profile = Profile.objects.get(account=request.user)

    context = {
        "profile": profile
    }

    return render(request, "onboard/provider/hello.html", context)

# Removed this because this is done through admin interface
# @transaction.atomic
# def onboard_provider_profile(request):

#     if request.method == 'POST':

#         form = ProfileForm(request.POST)

#         if form.is_valid():
#             # Update their profile
#             user = Profile.objects.get(account=request.user)
#             user.first_name = form.cleaned_data["first_name"]
#             user.last_name = form.cleaned_data["last_name"]
#             user.save()

#             # Say thank you
#             return redirect(reverse("onboard_provider_details"))
#     else:

#         form = ProfileForm()
#         context = {
#             "form": form
#         }

#     return render(request, "onboard/provider/profile.html", context)

@transaction.atomic
def onboard_provider_details(request):

    form = ProviderForm()
    context = {
        "form": form
    }

    if request.method == 'POST':

        form = ProviderForm(request.POST)

        if form.is_valid():
            # Change their isOnboarded value to true
            onboard = Onboard.objects.get(account=request.user)
            onboard.isOnboarded = True
            onboard.save()

            # Retrieve profile
            profile = Profile.objects.get(account=request.user)

            # Add the provider details
            create_provider = Provider.objects.create(profile=profile)

            # Update their provider details
            provider = Provider.objects.get(profile=profile)
            provider.phone = form.cleaned_data["phone"]
            provider.years_of_experience = form.cleaned_data["years_of_experience"]
            provider.registered_council = form.cleaned_data["registered_council"]
            provider.electronic_card = form.cleaned_data["electronic_card"]
            provider.save()

            # Say thank you
            return redirect(reverse("provider_dashboard"))

    return render(request, "onboard/provider/details.html", context)