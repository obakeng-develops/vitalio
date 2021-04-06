# Django
from django.urls import path

# Views
from .views import member_dashboard, member_bookings, member_profile, create_booking, leave_call_member, admin_add_provider, admin_usage_statistics, start_assessment, daily_life_assessment, focus_area_assessment, expectation_assessment, add_booking

urlpatterns = [
    path("", member_dashboard, name="member_dashboard"),
    path("bookings", member_bookings, name="member_bookings"),
    path("profile", member_profile, name="member_profile"),
    path("create/booking", create_booking, name="create_booking"),
    path("end-call/", leave_call_member, name="leave_call_member"),
    path("add/provider", admin_add_provider, name="admin_add_provider"),
    path("usage/statistics", admin_usage_statistics, name="admin_usage_statistics"),
    path("start/assessment", start_assessment, name="start_assessment"),
    path("assessment/daily-life", daily_life_assessment, name="daily_life_assessment"),
    path("assessment/focus-area", focus_area_assessment, name="focus_area_assessment"),
    path("assessment/expectation", expectation_assessment, name="expectation_assessment"),
    path("assessment/booking/add", add_booking, name="add_booking")
]