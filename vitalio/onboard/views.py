# Django
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.db import transaction

# Forms
from account.forms import ProfileForm, AddressForm
from company.forms import OrganizationForm
from provider.forms import ProviderForm

# Models 
from .models import Onboard
from account.models import Profile, Address
from company.models import Organization
from provider.models import Provider

# Member Onboarding
def onboard_member(request):
    """ Regular Member and Team Member onboarding """

    profile = Profile.objects.get(account=request.user)

    context = {
        "profile": profile
    }

    return render(request, "onboard/member/hello.html", context)

@transaction.atomic
def onboard_member_address(request):
    """ Regular Member and Team Member address details """

    if request.method == 'POST':

        form = AddressForm(request.POST)

        if form.is_valid():
            # Change their isOnboarded value to true
            onboard = Onboard.objects.get(account=request.user)
            onboard.isOnboarded = True
            onboard.save()

            # Retrieve profile
            profile = Profile.objects.get(account=request.user)
            profile.save()

            # Update their address
            address = Address.objects.get(profile=profile)
            address.line_one = form.cleaned_data['line_one']
            address.surburb = form.cleaned_data['surburb']
            address.city = form.cleaned_data['city']
            address.province = form.cleaned_data['province']
            address.country = form.cleaned_data['country']
            address.zip_code = form.cleaned_data['zip_code']
            address.save()

            # Say thank you
            return redirect(reverse("member_dashboard"))
    else:

        form = AddressForm()
        context = {
            "form": form
        }

    return render(request, "onboard/member/address.html", context)

# Admin Onboarding
def onboard_admin(request):
    """ Staff & Team admin onboarding """

    profile = Profile.objects.get(account=request.user)

    context = {
        "profile": profile
    }

    return render(request, "onboard/admin/hello.html", context)

@transaction.atomic
def onboard_admin_address(request):
    """ Staff & Team Member address details """

    if request.method == 'POST':

        form = AddressForm(request.POST)

        if form.is_valid():

            # Retrieve profile
            profile = Profile.objects.get(account=request.user)

            # Update their profile
            address = Address.objects.get(profile=profile)
            address.line_one = form.cleaned_data["line_one"]
            address.surburb = form.cleaned_data["surburb"]
            address.city = form.cleaned_data["city"]
            address.province = form.cleaned_data["province"]
            address.country = form.cleaned_data["country"]
            address.zip_code = form.cleaned_data["zip_code"]
            address.save()

            # Say thank you
            return redirect(reverse("member_dashboard"))
    else:

        form = AddressForm()
        context = {
            "form": form
        }

    return render(request, "onboard/admin/address.html", context)

@transaction.atomic
def onboard_admin_company(request):
    """ Staff & Team admin company details """

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
            # account_company = AccountCompany()
            # account_company.company = company
            # account_company.user = request.user
            # account_company.save()

            # Say thank you
            return redirect(reverse("member_dashboard"))
    else:

        form = CompanyForm()
        context = {
            "form": form
        }


    return render(request, "onboard/admin/company.html", context)

# Provider Onboarding
def onboard_provider(request):
    """ Provider onboarding """

    profile = Profile.objects.get(account=request.user)

    context = {
        "profile": profile
    }

    return render(request, "onboard/provider/hello.html", context)


@transaction.atomic
def onboard_provider_details(request):
    """ Provider details """

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