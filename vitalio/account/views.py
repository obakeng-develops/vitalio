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
from .forms import AccountCreationForm, ProfileForm, SubscriptionForm
from company.forms import OrganizationForm, OrganizationLocationForm

# Models
from .models import Account, Profile, Subscription
from onboard.models import Onboard
from company.models import Organization, Location, Membership

# Third Party
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from vitalio.roles import Provider, Member, Admin

def entry_point(request):

    onboard = Onboard.objects.get(account=request.user)

    if onboard.isOnboarded == False and (request.user.role == 3 or request.user.role == 8):
        return redirect(reverse("onboard_admin"))
    elif onboard.isOnboarded == True and (request.user.role == 3 or request.user.role == 8):
        return redirect(reverse("member_dashboard"))

    if onboard.isOnboarded == False and (request.user.role == 2 or request.user.role == 1 or request.user.role == 7):
        return redirect(reverse("onboard_member"))
    elif onboard.isOnboarded == True and (request.user.role == 2 or request.user.role == 1 or request.user.role == 7):
        return redirect(reverse("member_dashboard"))

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

# Admins
def register_admin(request):
    """ Register the team admin user """

    if request.method == "GET":
        return render(request, "account/register_admin.html", {"form": AccountCreationForm})

    elif request.method == "POST":
        form = AccountCreationForm(request.POST)

        if form.is_valid():
            # Assign form data to session variables
            request.session['email'] = form.cleaned_data["email"]
            request.session['password1'] = form.cleaned_data["password1"]
            request.session['password2'] = form.cleaned_data["password2"]


            return redirect(reverse("register_admin_profile"))

def register_admin_profile(request):
    """ Add admin details """

    # Retrieve the Profile Form
    form = ProfileForm()

    context = {
        "form": form
    }

    if request.POST:

        form = ProfileForm(request.POST)

        if form.is_valid():

            # Retrieve Profile Data and assign to session variables
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']

            return redirect('register_admin_organization')

    return render(request, "account/register_admin_profile.html", context)

def register_admin_organization(request):
    """ Register organization """

    # Retrieve the Organization Form
    form = OrganizationForm()

    context = {
        "form": form
    }

    if request.POST:

        form = OrganizationForm(request.POST)

        if form.is_valid():

            # Retrieve Profile Data and assign to session variables
            request.session['organization_name'] = form.cleaned_data['organization_name']

            return redirect('register_admin_organization_location')

    return render(request, "account/register_admin_organization.html", context)

@transaction.atomic
def register_admin_organization_location(request):
    """ Register organization location """

    # Retrieve the Organization location Form
    form = OrganizationLocationForm()

    context = {
        "form": form
    }

    if request.POST:

        form = OrganizationLocationForm(request.POST)

        if form.is_valid():

            # Create a new account for the admin user
            account = Account.objects.create_user(email=request.session['email'], password=request.session['password1'], role="3")
            account.save()

            # Update profile
            profile = Profile.objects.get(account=account)
            profile.first_name = request.session['first_name']
            profile.last_name = request.session['last_name']
            profile.save()

            # Create an organization object
            organization = Organization()
            organization.organization_name = request.session['organization_name']
            organization.save()

            # Add location data about the organization
            location = Location()
            location.organization = organization
            location.line_one = form.cleaned_data['line_one']
            location.surburb = form.cleaned_data['surburb']
            location.city =  form.cleaned_data['city']
            location.province = form.cleaned_data['province']
            location.country = form.cleaned_data['country']
            location.zip_code = form.cleaned_data['zip_code']

            # Add subscription
            subscription = Subscription()
            subscription.status = 2
            subscription.subscription_owner = account
            subscription.save()

            # Create a membership for this user within the organization
            membership = Membership()
            membership.organization = organization
            membership.user = account
            membership.save()

            # Send a success message
            messages.info(request, "Your account has been created. You can now log in.")

            return redirect('_/accounts/login')

    return render(request, "account/register_admin_organization_location.html", context)


# Members
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

def register_member(request):
    """ Register members """

    if request.method == "GET":
        return render(
            request, "account/register_member.html",
            {"form": AccountCreationForm}
        )
    elif request.method == "POST":
        form = AccountCreationForm(request.POST)

        if form.is_valid():
            # Get Form data
            request.session['email'] = form.cleaned_data["email"]
            request.session['password1'] = form.cleaned_data["password1"]

            return redirect(reverse("register_member_profile"))

@transaction.atomic
def register_member_profile(request):
    """ Register member's profile """

    profile = ProfileForm()

    context = {
        "form": profile
    }

    if request.POST:

        form = ProfileForm(request.POST)

        if form.is_valid():

            # Create New Account
            account = Account.objects.create_user(email=request.session['email'], password=request.session['password1'], role='1')
            account.save()

            # Add a subscription for the member
            subscription = Subscription()
            subscription.status = 2
            subscription.subscription_owner = account
            subscription.save()

            # Update profile
            profile = Profile.objects.get(account=account)
            profile.first_name = form.cleaned_data["first_name"]
            profile.last_name = form.cleaned_data["last_name"]
            profile.save()

            return redirect("thank_you")

    return render(request, "account/register_member_profile.html", context)

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

            # # Add to company
            # account_company = AccountCompany()
            # account_company.company = Company.objects.get(pk=1)
            # account_company.user = user
            # account_company.save()

            assign_role(user, 'provider')

            return redirect(reverse("thank_you"))

def thank_you(request):
    return render(request, "account/thankyou.html")

# Password Resets
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
					'domain':'vitalio.co',
					'site_name': 'Vitalio',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'https',
					}
					email = render_to_string(email_template_name, c)
                    
					try:
						send_mail(subject, email, settings.DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect("password_reset_done")

	password_reset_form = PasswordResetForm()

	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})