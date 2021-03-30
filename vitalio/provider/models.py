# Django
from django.db import models as m
from django.shortcuts import reverse
from datetime import date
import random
import string

# Models
from account.models import Account, Profile

class Schedule(m.Model):
    account = m.ForeignKey(Account, on_delete=m.CASCADE, related_name="provider_account")
    day = m.DateField()
    start_time = m.TimeField()
    end_time = m.TimeField()
    isBooked = m.BooleanField(default=False)

    def __str__(self):
        return str(self.day) + ", " + str(self.start_time) + " - " + str(self.end_time)

    @property
    def get_html_url(self):
        profile = Profile.objects.get(account=self.account)

        url = reverse('edit_schedule', args=(self.id,))
        return f'<a href="{url}"> {profile.first_name} - {self.start_time} </a>'

def generate_room_code():

    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))

        if Booking.objects.filter(room_code=code).count() == 0:
            break

    return code

class Booking(m.Model):
    patient = m.ForeignKey(Account, on_delete=m.CASCADE, related_name="patient_booking")
    provider = m.ForeignKey(Account, on_delete=m.CASCADE, related_name="booked_physician")
    timeslot = m.ForeignKey(Schedule, on_delete=m.CASCADE, related_name="provider_timeslot")
    room_code = m.CharField(max_length=20, default=generate_room_code, null=True, unique=True)
    isAccepted = m.BooleanField(default=False)
    isEnded = m.BooleanField(default=False)

    def __str__(self):
        return self.room_code

class Provider(m.Model):

    ENTRY = '0-2'
    MID = '3-5'
    SENIOR = '5+'

    YEARS_OF_EXPERIENCE = [
        (ENTRY, 'Entry (0-2yrs)'),
        (MID, 'Mid (3-5yrs)'),
        (SENIOR, 'Senior (5+ yrs)')
    ]

    HPCSA = 'HPCSA'
    CCSA = 'CCSA'

    REGISTERED_COUNCIL = [
        (HPCSA, 'Health Professions Council of South Africa'),
        (CCSA, 'Council for Counsellors in South Africa')
    ]

    profile = m.OneToOneField(Profile, on_delete=m.CASCADE, related_name="provider_profile")
    phone = m.CharField(max_length=10, blank=True, help_text='Contact phone number')
    years_of_experience = m.CharField(max_length=4, choices=YEARS_OF_EXPERIENCE, default=ENTRY)
    registered_council = m.CharField(max_length=5, choices=REGISTERED_COUNCIL, default=HPCSA)
    electronic_card = m.FileField(upload_to='provider_files', null=True, blank=True)

    def __str__(self):
        return self.registered_council + " (" + self.years_of_experience + ")"