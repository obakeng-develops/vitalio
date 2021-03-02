# Django
from django.urls import include, path

# Views
from .views import login_provider, register_admin, register_member, register_company_member, register_provider, entry_point, thank_you, change_password

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/provider", login_provider, name="login_provider"),
    path("register/admin", register_admin, name="register_admin"),
    path("register/member", register_member, name="register_member"),
    path("register/company/member", register_company_member, name="register_company_member"),
    path("register/provider", register_provider, name="register_provider"),
    path("e", entry_point, name="entry_point"),
    path("thank-you", thank_you, name="thank_you"),
    path("change-password", change_password, name="change_password")
]