# Django
from django.urls import include, path
from django.contrib.auth import views as auth_views

# Views
from .views import login_provider, register_admin, register_admin_profile, register_admin_organization, register_admin_organization_location, register_member, register_member_profile, register_provider, entry_point, thank_you, change_password, password_reset_request

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),

    # Login URLS
    path("login/provider", login_provider, name="login_provider"),

    # Admin Registration URLS 
    path("register/admin", register_admin, name="register_admin"),
    path("register/admin/profile", register_admin_profile, name="register_admin_profile"),
    path("register/admin/organization", register_admin_organization, name="register_admin_organization"),
    path("register/admin/organization/location", register_admin_organization_location, name="register_admin_organization_location"),

    # Member Registration URLS
    path("register/member", register_member, name="register_member"),
    path("register/member/profile", register_member_profile, name="register_member_profile"),

    # Provider Registration URLS
    path("register/provider", register_provider, name="register_provider"),

    # Common URLS 
    path("thank-you", thank_you, name="thank_you"),

    # Entry Point
    path("e", entry_point, name="entry_point"),

    #Account Settings
    path("change-password", change_password, name="change_password"),

    # Account Forgot Password
    path("password-reset", password_reset_request, name="password_reset_request"),
    path("password-reset/done",  auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete')
]