# Django
from django.urls import path

# Views
from .views import member_dashboard, member_profile, create_booking, leave_call_member

urlpatterns = [
    path("", member_dashboard, name="member_dashboard"),
    path("profile", member_profile, name="member_profile"),
    path("create-booking", create_booking, name="create_booking"),
    path("end-call/", leave_call_member, name="leave_call_member"),
]