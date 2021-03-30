# Django
from django.urls import include, path

# Views
from .views import onboard_admin, onboard_admin_profile, onboard_admin_company, onboard_member, onboard_member_profile, onboard_provider, onboard_provider_profile, onboard_provider_details

urlpatterns = [
    path("admin", onboard_admin, name="onboard_admin"),
    path("admin/profile", onboard_admin_profile, name="onboard_admin_profile"),
    path("admin/company", onboard_admin_company, name="onboard_admin_company"),
    path("member", onboard_member, name="onboard_member"),
    path("member/profile", onboard_member_profile, name="onboard_member_profile"),
    path("provider", onboard_provider, name="onboard_provider"),
    path("provider/profile", onboard_provider_profile, name="onboard_provider_profile"),
    path("provider/details", onboard_provider_details, name="onboard_provider_details")
]