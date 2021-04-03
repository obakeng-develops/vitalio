# Django
from django.urls import include, path
from django.contrib.auth import views as auth_views

# Views
from .views import login_provider, register_admin, register_member, register_company_member, register_provider, entry_point, thank_you, change_password, password_reset_request

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/provider", login_provider, name="login_provider"),
    path("register/admin", register_admin, name="register_admin"),
    path("register/member", register_member, name="register_member"),
    path("register/company/member", register_company_member, name="register_company_member"),
    path("register/provider", register_provider, name="register_provider"),
    path("e", entry_point, name="entry_point"),
    path("thank-you", thank_you, name="thank_you"),
    path("change-password", change_password, name="change_password"),
    path("password-reset", password_reset_request, name="password_reset_request"),
    path("password-reset/done",  auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete')
]