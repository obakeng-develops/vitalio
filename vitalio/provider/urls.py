# Django
from django.urls import path, re_path

# Views
from .views import provider_dashboard, provider_profile, provider_schedule, set_schedule, accept_booking, leave_call, provider_patients

urlpatterns = [
    path("", provider_dashboard, name="provider_dashboard"),
    path("profile", provider_profile, name="provider_profile"),
    re_path("schedule/$", provider_schedule, name="provider_schedule"),
    re_path("schedule/add/$", set_schedule, name="add_schedule"),
    re_path("schedule/edit/(?P<schedule_id>\d+)/$", set_schedule, name="edit_schedule"),
    re_path("accept-booking", accept_booking, name="accept_booking"),
    path("leave-call/", leave_call, name="leave_call_provider"),
    path("patients", provider_patients, name="provider_patients"),
]