# Django
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models.query_utils import Q
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings

# Forms
from .forms import AccountCreationForm

# Models
from .models import Account, Profile
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

            # Add to company
            account_company = AccountCompany()
            account_company.company = Company.objects.get(pk=1)
            account_company.user = user
            account_company.save()

            assign_role(user, 'provider')

            return redirect(reverse("thank_you"))

def thank_you(request):
    return render(request, "account/thankyou.html")

@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, request.user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
           
            return redirect(reverse("entry_point"))

def password_reset_request(request):

	if request.method == "POST":

		password_reset_form = PasswordResetForm(request.POST)

		if password_reset_form.is_valid():

			data = password_reset_form.cleaned_data['email']
			associated_users = Account.objects.filter(Q(email=data))

			if associated_users.exists():
				for user in associated_users:

					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Vitalio',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
                    
					try:
						send_mail(subject, email, settings.DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect("password_reset_done")

	password_reset_form = PasswordResetForm()

	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})