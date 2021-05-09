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
    """ User's account  """

    ROLE_CHOICES = [
        (1, "Member"),
        (2, "Team Member"),
        (3, "Team Admin"),
        (4, "Psychologist"),
        (5, "General Practitioner"),
        (6, "Counsellor"),
        (7, "Staff Member"),
        (8, "Staff Admin"),
    ]

    email = m.EmailField(_('email address'), unique=True)
    is_staff = m.BooleanField(default=False)
    is_active = m.BooleanField(default=True)
    date_joined = m.DateTimeField(default=timezone.now)
    role = m.PositiveSmallIntegerField(default=1, choices=ROLE_CHOICES)

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

class Plan(m.Model):
    """ Subscription Plan """

    plan_name = m.CharField(max_length=50)
    plan_amount = m.CharField(max_length=10, null=True)
    plan_code = m.CharField(max_length=128)
    plan_description = m.TextField()
    date_created = m.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.plan_name + " [" + self.plan_code + "]"

class Subscription(m.Model):
    """ User's subscription """
    
    ACTIVE = 1
    NOT_ACTIVE = 2

    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (NOT_ACTIVE, "Not Active")
    ]

    start_date = m.DateTimeField(default=timezone.now)
    status = m.CharField(max_length=1, choices=STATUS_CHOICES, default=ACTIVE)
    subscription_owner = m.ForeignKey(Account, on_delete=m.SET_NULL, null=True, blank=True)
    subscription_plan = m.ForeignKey(Plan, on_delete=m.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.subscription_owner.email) + " (" + self.subscription_plan + ")"

class Profile(m.Model):
    """ User's profile """

    account = m.OneToOneField(Account, on_delete=m.CASCADE, related_name="user_account")
    first_name = m.CharField(max_length=50, blank=True, null=True)
    last_name = m.CharField(max_length=50, blank=True, null=True)
    random_id = m.CharField(max_length=20, default=generate_profile_id, blank=True, null=True)
    profile_slug = AutoSlugField(populate_from='random_id')
    profile_image = m.ImageField(default='default.jpg', upload_to='profile_images')

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

class Address(m.Model):
    """ User's address """

    profile = m.ForeignKey(Profile, on_delete=m.CASCADE, related_name="user_address")
    line_one = m.CharField(max_length=50, blank=True, null=True)
    surburb = m.CharField(max_length=50, blank=True, null=True)
    city = m.CharField(max_length=50, blank=True, null=True)
    province = m.CharField(max_length=20, blank=True, null=True)
    country = m.CharField(max_length=50, blank=True, null=True)
    zip_code = m.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.line_one) + ", " + str(self.surburb) + ", " + str(self.city) + ", " + str(self.province) + ", " + str(self.country) + ", " + str(self.zip_code)

class WaitList(m.Model):
    """ User waitlist """

    email = m.CharField(max_length=80)

    def __str__(self):
        return self.email