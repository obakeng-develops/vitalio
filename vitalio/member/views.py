# Django
from django.shortcuts import render, redirect, reverse
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os

# Models
from account.models import Account, Profile
from provider.models import Schedule, Booking, Provider
from company.models import Company, Location, AccountCompany

# Forms
from account.forms import ProfileForm, AccountCreationForm
from provider.forms import ScheduleForm, BookingForm, ProviderForm
from company.forms import CompanyForm

# Third Party
from rolepermissions.decorators import has_role_decorator
from rolepermissions.checkers import has_role
from vitalio.roles import Admin
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from vitalio.roles import Provider, Member, Admin

# Twilio Account Values
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')

@transaction.atomic
def member_dashboard(request):

    profile = Profile.objects.get(account=request.user)

    schedules = Schedule.objects.filter(isBooked=False)

    bookings = Booking.objects.filter(patient=request.user, isEnded=False)

    account_company = AccountCompany.objects.get(user=request.user)

    context = {
        "profile": profile,
        "schedules": schedules,
        "bookings": bookings,
        "company": account_company
    }

    return render(request, "member/dashboard.html", context)

@login_required
def member_profile(request):

    if request.method == 'POST':

        form = ProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            # Update User Profile
            profile = Profile.objects.get(account=request.user)
            profile.first_name = form.cleaned_data["first_name"]
            profile.last_name = form.cleaned_data["last_name"]
            profile.save()

            return redirect(reverse('member_profile'))
    
    else:

        form = ProfileForm(instance=request.user)

        password = PasswordChangeForm(request.user)

        profile = Profile.objects.get(account=request.user)

        company_user = AccountCompany.objects.get(user=request.user)

        context = {
            "form": form,
            "profile": profile,
            "password": password,
            "company_user": company_user
        }    

    return render(request, "member/profile.html", context)

@login_required
@transaction.atomic
def create_booking(request):

    schedule_id = request.POST["schedule"]
        
    # Set timeslot to booked
    schedule = Schedule.objects.get(id=schedule_id)
    schedule.isBooked = True
    schedule.save()

    # Create a booking
    booking = Booking()
    booking.patient = request.user
    booking.provider = schedule.account
    booking.timeslot = schedule
    booking.isAccepted = False
    booking.save()

    return redirect(reverse("member_dashboard"))

@login_required
def leave_call_member(request):

    if request.POST:

        roomcode = request.session.get('booking')

        client = Client(account_sid, auth_token)

        exists = client.video.rooms.list(unique_name=roomcode)

        if exists is None:
            return redirect('member_dashboard')
        else:
            return redirect('member_dashboard')
    
    return redirect(reverse("member_dashboard"))

@has_role_decorator('admin')
@transaction.atomic
def admin_add_provider(request):

    account_form = AccountCreationForm()
    profile_form = ProfileForm()

    context = {
        "account_form": account_form,
        "profile_form": profile_form
    }

    if request.method == 'POST':

        acc_form = AccountCreationForm(request.POST)
        prof_form = ProfileForm(request.POST)

        if acc_form.is_valid() and prof_form.is_valid():

            email = acc_form.cleaned_data["email"]
            password1 = acc_form.cleaned_data["password1"]
            password1 = acc_form.cleaned_data["password2"]

            first_name = prof_form.cleaned_data["first_name"]
            last_name = prof_form.cleaned_data["last_name"]

            # Create a new user
            user = Account.objects.create_user(email=email, password=password1, user_type='3')
            user.save()

            # Retrieve & update profile
            profile = Profile.objects.get(account=user)
            profile.first_name = first_name
            profile.last_name = last_name
            profile.save()

            # Add to company
            account_company = AccountCompany()
            account_company.company = Company.objects.get(pk=2)
            account_company.user = user
            account_company.save()

            assign_role(user, 'provider')
            messages.info(request, "Provider has been added!")


    return render(request, "member/add_provider.html", context)

@has_role_decorator('admin')
def admin_usage_statistics(request):
    return render(request, "member/usage_statistics.html")