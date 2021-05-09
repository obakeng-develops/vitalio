# Django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.db import transaction

# Models
from account.models import WaitList

# Functions
def home(request):
    return render(request, "pages/home.html")

def about(request):
    return render(request, "pages/about.html")

def pricing(request):
    return render(request, "pages/pricing.html")

def demo(request):
    return render(request, "pages/demo.html")

def business(request):
    return render(request, "pages/business.html")

def patients(request):
    return render(request, "pages/patients.html")

@transaction.atomic
def waitlist(request):

    email = request.POST.get("waitlist")

    if request.POST:

        # Add to Database
        wait_list = WaitList()
        wait_list.email = email
        wait_list.save()

        # Send Email
        subject = "New Member"
        email_template_name = "pages/waitlist.txt"
        c = {
            "email": email
        }
        email = render_to_string(email_template_name, c)
                        
        try:
            send_mail(subject, email, settings.DEFAULT_FROM_EMAIL , ["hello@vitalio.co",], fail_silently=False)
            return render(request, "pages/thank_you_waitlist.html")
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect("password_reset_done")