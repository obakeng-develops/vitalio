# Django
from django.shortcuts import render, redirect, reverse
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from datetime import datetime
import os

# Models
from account.models import Account, Profile
from provider.models import Schedule, Booking, Provider
from company.models import Company, Location, AccountCompany, CompanyBooking
from .models import Assessment

# Forms
from account.forms import ProfileForm, AccountCreationForm
from provider.forms import ScheduleForm, BookingForm, ProviderForm
from company.forms import CompanyForm
from member.forms import AssessmentFeelingForm, DailyLifeAssessmentForm, FocusAssessmentForm, ExpectationAssessmentForm

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

@login_required
def member_dashboard(request):

    profile = Profile.objects.get(account=request.user)

    bookings = Booking.objects.filter(patient=request.user, isEnded=False).count()

    account_company = AccountCompany.objects.get(user=request.user)

    context = {
        "profile": profile,
        "company": account_company,
        "booking": bookings
    }

    return render(request, "member/dashboard.html", context)

@login_required
def member_bookings(request):

    bookings = Booking.objects.filter(patient=request.user, isEnded=False)

    booking_count = Booking.objects.filter(patient=request.user, isEnded=False).count()

    date_today = datetime.today().date()

    context = {
        "bookings": bookings,
        "date": date_today,
        "booking": booking_count
    }

    return render(request, "member/bookings.html", context)

@login_required
def member_profile(request):

    profile = Profile.objects.get(account=request.user)

    booking_count = Booking.objects.filter(patient=request.user, isEnded=False).count()

    form = ProfileForm(instance=profile)

    password = PasswordChangeForm(request.user)

    company_user = AccountCompany.objects.get(user=request.user)

    context = {
        "form": form,
        "profile": profile,
        "password": password,
        "company_user": company_user,
        "booking": booking_count
    }  

    if request.method == 'POST':

        form = ProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            # Update User Profile
            profile = Profile.objects.get(account=request.user)
            profile.first_name = form.cleaned_data["first_name"]
            profile.last_name = form.cleaned_data["last_name"]
            profile.save()

            return redirect(reverse('member_profile'))  

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

    # Add booking to assessment record
    assessment = Assessment.objects.get(id=request.session['assessment_id'])
    assessment.booking = booking
    assessment.save()

    # Retrieve Profile
    profile = Profile.objects.get(account=request.user)

    subject = "Session Created"
    email_template_name = "member/email/booking_email.txt"
    c = {
	    'email': request.user.email,
		'user': profile,
        'booking': booking,
        'site_name': 'Vitalio'
	}
    email = render_to_string(email_template_name, c)
                    
    try:
        send_mail(subject, email, settings.DEFAULT_FROM_EMAIL , [request.user.email], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

    messages.info(request, "Your booking has been made")

    return redirect(reverse("member_dashboard"))

@login_required
@transaction.atomic
def leave_call_member(request):

    if request.POST:

        # Retrieve booking code
        roomcode = request.session.get('booking')

        client = Client(account_sid, auth_token)

        # Retrieve company & booking
        company = Company.objects.get(user=request.user)
        booking = Booking.objects.get(room_code=roomcode)

        # Add the booking to company stats
        company_booking = CompanyBooking()
        company_booking.company = company
        company_booking.booking = booking
        company_booking.save()

        # Check if the room still exists, this is in case the provider left first
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
    booking_count = Booking.objects.filter(patient=request.user, isEnded=False).count()

    context = {
        "account_form": account_form,
        "profile_form": profile_form,
        "booking": booking_count
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
            account_company.company = Company.objects.get(pk=1)
            account_company.user = user
            account_company.save()

            assign_role(user, 'provider')
            messages.info(request, "Provider has been added!")


    return render(request, "member/add_provider.html", context)

@has_role_decorator('admin')
def admin_usage_statistics(request):

    currentMonth = datetime.now().month

    company = AccountCompany.objects.get(user=request.user)

    booking_count = Booking.objects.filter(patient=request.user, isEnded=False).count()

    company_bookings = CompanyBooking.objects.filter(company=company.company, booking__timeslot__day__month=currentMonth).count()

    context = {
        "bookings": company_bookings,
        "month": currentMonth,
        "booking": booking_count
    }

    return render(request, "member/usage_statistics.html", context)

@login_required
@transaction.atomic
def start_assessment(request):

    form = AssessmentFeelingForm()

    context = {
        "form": form
    }

    if request.POST:

        form = AssessmentFeelingForm(request.POST)

        if form.is_valid():

            profile = Profile.objects.get(account=request.user)
            
            # Create Assessment
            create_assessment = Assessment()
            create_assessment.user = profile
            create_assessment.feeling_today = form.cleaned_data["feeling_today"]
            create_assessment.save()

            request.session['assessment_id'] = create_assessment.id

            return redirect("daily_life_assessment")


    return render(request, "member/assessments/start_assessment.html", context)

@login_required
@transaction.atomic
def daily_life_assessment(request):

    form = DailyLifeAssessmentForm()

    context = {
        "form": form
    }

    if request.POST:

        form = DailyLifeAssessmentForm(request.POST)

        if form.is_valid():
            
            # Create Assessment
            create_assessment = Assessment.objects.get(id=request.session['assessment_id'])
            create_assessment.daily_life_feeling = form.cleaned_data['daily_life_feeling']
            create_assessment.save()

            return redirect("focus_area_assessment")

    return render(request, "member/assessments/daily_life_assessment.html", context)

@login_required
@transaction.atomic
def focus_area_assessment(request):

    form = FocusAssessmentForm()

    context = {
        "form": form
    }

    if request.POST:

        form = FocusAssessmentForm(request.POST)

        if form.is_valid():
            
            # Create Assessment
            create_assessment = Assessment.objects.get(id=request.session['assessment_id'])
            create_assessment.focus_area = form.cleaned_data['focus_area']
            create_assessment.save()

            return redirect("expectation_assessment")

    return render(request, "member/assessments/focus_area_assessment.html", context)

@login_required
@transaction.atomic
def expectation_assessment(request):

    form = ExpectationAssessmentForm()

    context = {
        "form": form
    }

    if request.POST:

        form = ExpectationAssessmentForm(request.POST)

        if form.is_valid():
            
            # Create Assessment
            create_assessment = Assessment.objects.get(id=request.session['assessment_id'])
            create_assessment.expectation = form.cleaned_data['expectation']
            create_assessment.save()

            return redirect("add_booking")

    return render(request, "member/assessments/expectation_assessment.html", context)

@login_required
@transaction.atomic
def add_booking(request):

    schedules = Schedule.objects.filter(isBooked=False)

    bookings = Booking.objects.filter(patient=request.user, isEnded=False)

    context = {
        "schedules": schedules
    }

    return render(request, "member/assessments/add_booking.html", context)