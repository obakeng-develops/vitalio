# Django
from django.shortcuts import render, redirect, reverse
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError

from datetime import datetime
import os
from django.conf import settings

# Models
from account.models import Account, Profile, Subscription
from provider.models import Schedule, Booking, Provider
from company.models import Organization, Location, CompanyBooking, Membership
from .models import Assessment

# Forms
from account.forms import ProfileForm, AccountCreationForm
from provider.forms import ScheduleForm, BookingForm, ProviderForm
from company.forms import OrganizationForm
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
account_sid="ACb4d2387e934ec98773f3fc4732cbce80"
auth_token="2bdf89f370d340ad3546d27639d45c09"
api_key_sid="SK413cfa1855c87162baeb39e5c8fbbb65"
api_key_secret="jIqm631MCt29lIWn8OLd9g1j6DC1ONEc"

# Member Functions
@login_required
def member_dashboard(request):
    """ Member's Dashboard """

    profile = Profile.objects.get(account=request.user)

    membership = Membership.objects.get(user=request.user)

    bookings = Booking.objects.filter(patient=request.user, isEnded=False).count()

    context = {
        "profile": profile,
        "booking": bookings,
        "membership": membership
    }

    return render(request, "member/dashboard.html", context)

@login_required
def member_bookings(request):
    """ Member Bookings List """

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
    """ Member Profile """

    account = Account.objects.get(email=request.user.email)

    # For Admins
    if account.role == 3 or account.role == 8:

        # Retrieve profile
        profile = Profile.objects.get(account=request.user)

        # Retrieve the membership
        membership = Membership.objects.get(user=request.user)

        # Fetch the subscription
        try:
            subscription = Subscription.objects.get(subscription_owner=request.user)
        except ObjectDoesNotExist:
            raise Http404("No Subscription matches the given query.")

        # Filter the bookings
        booking_count = Booking.objects.filter(patient=request.user, isEnded=False).count()

        form = ProfileForm(instance=profile)

        password = PasswordChangeForm(request.user)

        context = {
            "form": form,
            "membership": membership,
            "subscription": subscription,
            "profile": profile,
            "password": password,
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

    # For Admins
    if account.role == 1 or account.role == 2:

        # Retrieve Profile
        profile = Profile.objects.get(account=request.user)

        # Retrieve Membership
        membership = Membership.objects.get(user=request.user)

        # Filter the bookings
        booking_count = Booking.objects.filter(patient=request.user, isEnded=False).count()

        # Retrieve the profile
        form = ProfileForm(instance=profile)

        password = PasswordChangeForm(request.user)

        context = {
            "form": form,
            "membership": membership,
            "profile": profile,
            "password": password,
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

# Room Functions
@login_required
@transaction.atomic
def leave_call_member(request):
    """ End call from member's side """

    if request.POST:

        # Retrieve booking code
        roomcode = request.session.get('booking')

        client = Client(account_sid, auth_token)

        # Retrieve company & booking
        # account_company = AccountCompany.objects.get(user=request.user)
        # booking = Booking.objects.get(room_code=roomcode)

        # # Add the booking to company stats
        # company_booking = CompanyBooking()
        # company_booking.company = account_company.company
        # company_booking.booking = booking
        # company_booking.save()

        # Check if the room still exists, this is in case the provider left first
        exists = client.video.rooms.list(unique_name=roomcode)

        if exists is None:
            return redirect('member_dashboard')
        else:
            return redirect('member_dashboard')

    
    return redirect(reverse("member_dashboard"))

# Admin Functions
@login_required
@transaction.atomic
def admin_add_provider(request):
    """ Staff Admin can add a provider from here """

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
            # account_company = AccountCompany()
            # account_company.company = Company.objects.get(pk=1)
            # account_company.user = user
            # account_company.save()

            assign_role(user, 'provider')
            messages.info(request, "Provider has been added!")


    return render(request, "member/add_provider.html", context)

@login_required
def admin_usage_statistics(request):
    """ Team Admin's can gauge usage statistics """

    # currentMonth = datetime.now().month

    # booking_count = Booking.objects.filter(patient=request.user, isEnded=False).count()

    # company_bookings = CompanyBooking.objects.filter(company=company.company, booking__timeslot__day__month=currentMonth).count()

    # context = {
    #     "bookings": company_bookings,
    #     "month": currentMonth,
    #     "booking": booking_count
    # }

    return render(request, "member/usage_statistics.html")

@login_required
def invite_members(request):
    """ Invite members to your organization """

    members = request.POST.get('members')

    account = Account.objects.get(email=request.user.email)

    profile = Profile.objects.get(account=account)

    membership = Membership.objects.get(user=request.user)

    if request.POST:

        subject = "You've been invited to join " + str(membership.organization) + "."
        email_template_name = "member/email/invite_member.txt"
        c = {
			"user": profile.first_name,
			'domain': '127.0.0.1:8000',
			'site_name': 'Vitalio',
            'organization': membership.organization.organization_name,
			'protocol': 'http',
            'email': members
        }
        email = render_to_string(email_template_name, c)
                    
        try:
            send_mail(subject, email, settings.DEFAULT_FROM_EMAIL , [members], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        return redirect("invite_done")

@login_required
def invite_done(request):
    """ Invite sent """

    return render(request, "member/invite_done.html")

def invite_members_register(request, organization):
    """ Registration page after invite """

    profile = ProfileForm()

    context = {
        "org": organization,
        "profile": profile
    }

    if request.POST:

        form = ProfileForm(request.POST)

        if form.is_valid():

            # Assign form data to session variables
            request.session['organization'] = organization
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']

            return redirect('invite_sign_up')

    return render(request, "member/invite_members_register.html", context)

@transaction.atomic
def invite_sign_up(request):
    """ Invited members sign up """

    form = AccountCreationForm()

    context = {
        "form": form
    }

    if request.POST:

        form = AccountCreationForm(request.POST)

        if form.is_valid():

            # Create a new account
            account = Account.objects.create_user(email=form.cleaned_data['email'], password=form.cleaned_data['password1'], role='2')
            account.save()

            # Update profile
            profile = Profile.objects.get(account=account)
            profile.first_name = request.session['first_name']
            profile.last_name = request.session['last_name']
            profile.save()

            # Retrieve organization
            organization = Organization.objects.get(organization_name=request.session['organization'])

            # Create a new membership in the organization
            membership = Membership.objects.create(organization=organization, user=account)
            membership.save()

            return redirect('invite_thank_you')

    return render(request, "member/invite_sign_up.html", context)

def invite_thank_you(request):
    """ Invite complete function """

    return render(request, "member/invite_thank_you")

# Assessment Functions
@login_required
@transaction.atomic
def start_assessment(request):
    """ Start a member assessment """

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
    """ Second step of assessment """

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
    """ Third step of assessment """

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
    """ Fourth step of assessment """

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
    """ Fifth step of assessment """

    schedules = Schedule.objects.filter(isBooked=False)

    bookings = Booking.objects.filter(patient=request.user, isEnded=False)

    context = {
        "schedules": schedules
    }

    return render(request, "member/assessments/add_booking.html", context)

@login_required
@transaction.atomic
def create_booking(request):
    """ Create a booking """

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