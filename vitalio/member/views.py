# Django
from django.shortcuts import render, redirect, reverse
from django.db import transaction
from django.http import HttpResponse
import os

# Models
from account.models import Account, Profile
from provider.models import Schedule, Booking

# Forms
from account.forms import ProfileForm
from provider.forms import ScheduleForm, BookingForm

# Third Party
from rolepermissions.decorators import has_role_decorator
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

# Twilio Account Values
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
api_key_sid = os.environ['TWILIO_API_KEY_SID']
api_key_secret = os.environ['TWILIO_API_KEY_SECRET']

@transaction.atomic
def member_dashboard(request):

    profile = Profile.objects.get(account=request.user)

    schedules = Schedule.objects.filter(isBooked=False)

    bookings = Booking.objects.filter(patient=request.user)

    context = {
        "profile": profile,
        "schedules": schedules,
        "bookings": bookings,
    }

    return render(request, "member/dashboard.html", context)

def member_profile(request):

    if request.method == 'POST':

        form = ProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            # Update User Profile
            profile = Profile.objects.get(account=request.user)
            profile.first_name = form.cleaned_data["first_name"]
            profile.last_name = form.cleaned_data["last_name"]
            profile.save()
    
    else:

        form = ProfileForm(instance=request.user)

        context = {
            "form": form,
        }    

    return render(request, "member/profile.html", context)

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
    booking.room_code = '8928rgff'
    booking.isAccepted = False
    booking.save()

    return redirect(reverse("member_dashboard"))

def leave_call_member(request):

    if request.POST:

        roomcode = request.session.get('booking')

        client = Client(account_sid, auth_token)

        room = client.video.rooms(roomcode).fetch()

        if room.status == 'completed':
            return redirect(reverse("member_dashboard"))
    
    return redirect(reverse("member_dashboard"))
