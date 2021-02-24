# Django
from django.db import models as m
from django.shortcuts import reverse
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

    def __str__(self):
        return self.room_code
