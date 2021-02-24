# Django
from django.db import models as m
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import random
import string

# Third Party
from autoslug import AutoSlugField

# Managers
from .managers import CustomAccountManager

class Account(AbstractBaseUser, PermissionsMixin):

    USER_TYPE_CHOICES = [
        (1, "Member"),
        (2, "Admin"),
        (3, "Provider"),
    ]

    email = m.EmailField(_('email address'), unique=True)
    is_staff = m.BooleanField(default=False)
    is_active = m.BooleanField(default=True)
    date_joined = m.DateTimeField(default=timezone.now)
    user_type = m.PositiveSmallIntegerField(default=1, choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomAccountManager()

    def __str__(self):
        return self.email


def generate_profile_id():

    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))

        if Profile.objects.filter(random_id=code).count() == 0:
            break

    return code

class Profile(m.Model):
    account = m.OneToOneField(Account, on_delete=m.CASCADE, related_name="user_account")
    first_name = m.CharField(max_length=50, blank=True, null=True)
    last_name = m.CharField(max_length=50, blank=True, null=True)
    random_id = m.CharField(max_length=20, default=generate_profile_id, blank=True, null=True)
    profile_slug = AutoSlugField(populate_from='random_id')
    profile_image = m.ImageField(default='default.jpg', upload_to='profile_images')

    def __str__(self):
        return self.first_name + " " + self.last_name

class Address(m.Model):
    profile = m.ForeignKey(Profile, on_delete=m.CASCADE, related_name="user_address")
    line_one = m.CharField(max_length=50, blank=True, null=True)
    surburb = m.CharField(max_length=50, blank=True, null=True)
    city = m.CharField(max_length=50, blank=True, null=True)
    province = m.CharField(max_length=20, blank=True, null=True)
    country = m.CharField(max_length=50, blank=True, null=True)
    zip_code = m.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.line_one + ", " + self.surburb + ", " + self.city + ", " + self.province + ", " + self.country + ", " + self.zip_code