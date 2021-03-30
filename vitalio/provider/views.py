# Django
from django.shortcuts import render, redirect, reverse, get_object_or_404
from datetime import datetime, date, timedelta
from django.views import generic
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.contrib import messages
import calendar
import os

# Models 
from account.models import Profile
from .models import Schedule, Booking

# Forms
from .forms import ScheduleForm
from account.forms import ProfileForm

# Utils
from .utils import Calendar

# Third Party
from rolepermissions.decorators import has_role_decorator
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

# Twilio Account Values
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')

@has_role_decorator('provider')
def provider_dashboard(request):

    profile = Profile.objects.get(account=request.user)

    bookings = Booking.objects.filter(provider=request.user, isEnded=False)

    context = {
        "profile": profile,
        "bookings": bookings
    }

    return render(request, "provider/dashboard.html", context)

@has_role_decorator('provider')
def provider_profile(request):

    profile = Profile.objects.get(account=request.user)
    form = ProfileForm(instance=profile)

    password = PasswordChangeForm(request.user)

    context = {
        "form": form,
        "profile": profile,
        "password": password
    }   

    if request.method == 'POST':

        form = ProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            # Update User Profile
            profile = Profile.objects.get(account=request.user)
            profile.first_name = form.cleaned_data["first_name"]
            profile.last_name = form.cleaned_data["last_name"]
            profile.save() 
            messages.info(request, "Your profile has been updated!")

    return render(request, "provider/profile.html", context)

@has_role_decorator('provider')
def provider_schedule(request):

    # Use today's date for the calendar
    d = get_date(request.GET.get('month', None))

    # Instantiate our calendar class with today's year and date
    cal = Calendar(d.year, d.month)

    # Call the formatmonth method, which returns our calendar as a table
    html_cal = cal.formatmonth(withyear=True)

    context = {
        "calendar": mark_safe(html_cal),
        "prev_month": prev_month(d),
        "next_month": next_month(d),
    }

    return render(request, "provider/schedule.html", context)

# Calendar functions
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@has_role_decorator('provider')
@transaction.atomic
def set_schedule(request, schedule_id=None):

    instance = Schedule()
    
    if schedule_id:
        instance = get_object_or_404(Schedule, pk=schedule_id)
    else:
        instance = Schedule()
    
    form = ScheduleForm(request.POST or None, instance=instance)

    if request.POST and form.is_valid():

        schedule = Schedule()
        schedule.account = request.user
        schedule.day = form.cleaned_data["day"]
        schedule.start_time = form.cleaned_data["start_time"]
        schedule.end_time = form.cleaned_data["end_time"]
        schedule.save()

        return HttpResponseRedirect(reverse('provider_schedule'))

    return render(request, 'provider/set_schedule.html', {'form': form})

@transaction.atomic
def accept_booking(request):

    if request.POST:

        booking_id = request.POST['booking_id']

        booking = Booking.objects.get(id=booking_id)
        booking.isAccepted = True
        booking.save()

    return redirect(reverse("provider_dashboard"))

def leave_call(request):

    if request.POST:

        roomcode = request.session.get('booking')

        client = Client(account_sid, auth_token)

        room = client.video.rooms(roomcode).update(status='completed')

        # End the booking
        booking = Booking.objects.get(room_code=roomcode)
        booking.isEnded = True
        booking.save()

    return redirect(reverse("provider_dashboard"))

@has_role_decorator('provider')
def provider_patients(request):

    bookings = Booking.objects.filter(provider=request.user, isEnded=True)

    context = {
        "bookings": bookings
    }

    return render(request, "provider/patients.html", context)