# Django
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm

# Forms
from .forms import AccountCreationForm

# Models
from .models import Account
from onboard.models import Onboard
from company.models import Company, AccountCompany

# Third Party
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from vitalio.roles import Provider, Member, Admin

def entry_point(request):

    onboard = Onboard.objects.get(account=request.user)

    if onboard.isOnboarded == False and has_role(request.user, Member):
        return redirect(reverse("onboard_member"))
    elif onboard.isOnboarded == False and has_role(request.user, Admin):
        return redirect(reverse("onboard_admin"))
    elif onboard.isOnboarded == False and has_role(request.user, Provider):
        return redirect(reverse("onboard_provider"))
    elif onboard.isOnboarded == True and has_role(request.user, Member):
        return redirect(reverse("member_dashboard"))
    elif onboard.isOnboarded == True and has_role(request.user, Admin):
        return redirect(reverse("member_dashboard"))
    elif onboard.isOnboarded == True and has_role(request.user, Provider):
        return redirect(reverse("provider_dashboard"))

# Login page for Providers
def login_provider(request):

    if request.method == 'POST':
        
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse("provider_dashboard"))

    else:
        form = AuthenticationForm()

        context = {
            "form": form
        }

    return render(request, "registration/login_provider.html", context)


@transaction.atomic
def register_admin(request):
    if request.method == "GET":
        return render(
            request, "account/register_admin.html",
            {"form": AccountCreationForm}
        )
    elif request.method == "POST":
        form = AccountCreationForm(request.POST)

        if form.is_valid():
            # Get Form data
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            # Create New Account
            user = Account.objects.create_user(email=email, password=password1, user_type='2')
            user.save()

            assign_role(user, 'admin')

            return redirect(reverse("thank_you"))

def register_company_member(request):

    if request.POST:

        company_id = request.POST["company"]
        request.session["company"] = company_id

        return redirect(reverse("register_member"))

    else:
        companies = Company.objects.all()

        context = {
            "companies": companies
        }

    return render(request, "account/register_member_company.html", context)

@transaction.atomic
def register_member(request):

    if request.method == "GET":
        return render(
            request, "account/register_member.html",
            {"form": AccountCreationForm}
        )
    elif request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            # Get Form data
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            # Create New Account
            user = Account.objects.create_user(email=email, password=password1, user_type='1')
            user.save()

            # Add to company
            account_company = AccountCompany()
            account_company.company = Company.objects.get(pk=request.session["company"])
            account_company.user = user
            account_company.save()

            assign_role(user, 'member')

            return redirect(reverse("thank_you"))

@transaction.atomic
def register_provider(request):
    if request.method == "GET":
        return render(
            request, "account/register_provider.html",
            {"form": AccountCreationForm}
        )
    elif request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            # Get Form data
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            # Create New Account
            user = Account.objects.create_user(email=email, password=password1, user_type='3')
            user.save()

            assign_role(user, 'provider')

            return redirect(reverse("thank_you"))

def thank_you(request):
    return render(request, "account/thankyou.html")
