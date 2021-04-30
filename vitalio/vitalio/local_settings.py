import os
import environ


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "vitalio_prod",
        "USER": "dbadmin",
        "PASSWORD": "vitalio@db2021!",
        "HOST": "localhost",
    }
}

ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
API_KEY_SID = os.environ.get('TWILIO_API_KEY_SID')
API_KEY_SECRET = os.environ.get('TWILIO_API_KEY_SECRET')

# Email Backend
EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'

DEFAULT_FROM_EMAIL = 'noreply@vitalio.co'
SERVER_EMAIL = 'noreply@vitalio.co'

ANYMAIL = {
    "SENDGRID_API_KEY": os.environ.get("SENDGRID_API_KEY"),
}
