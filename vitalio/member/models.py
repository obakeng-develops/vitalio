# Django
from django.db import models as m
from django.utils import timezone
import random
import string

# Models
from account.models import Profile
from provider.models import Booking

class Assessment(m.Model):
    """ User assessment """

    LOW = 'LW'
    MEDIUM = 'MD'
    HIGH = 'HG'

    PRIORITY_CHOICES = [
        (LOW, 'Good'),
        (MEDIUM, 'Okay'),
        (HIGH, 'Not Okay')
    ]

    JOYFUL = 'J'
    CALM = 'C'
    ANXIOUS = 'A'
    HELPLESS = 'H'
    DEPRESSING = 'D'
    MIXED = 'M'

    DAILY_LIFE_CHOICES = [
        (JOYFUL, 'Joyful'),
        (CALM, 'Calm'),
        (ANXIOUS, 'Anxious'),
        (HELPLESS, 'Helpless'),
        (DEPRESSING, 'Depressed'),
        (MIXED, 'Mixed')
    ]

    STRESS = 'SAX'
    RELATIONSHIPS = 'RTN'
    WORK_PERFORMANCE = 'WPF'
    LIFE_CHALLENGES = 'LCH'
    INCLUSION_BELONGING = 'IBL'

    FOCUS_AREA_CHOICES = [
        (STRESS, 'Stress & Anxiety'),
        (RELATIONSHIPS, 'Relationships'),
        (WORK_PERFORMANCE, 'Work Performance'),
        (LIFE_CHALLENGES, 'Life Challenges'),
        (INCLUSION_BELONGING, 'Inclusion & Belonging')
    ]

    user = m.ForeignKey(Profile, on_delete=m.CASCADE, related_name="user_assessment"),
    feeling_today = m.CharField(max_length=2, choices=PRIORITY_CHOICES, default=LOW)
    daily_life_feeling = m.CharField(max_length=1, choices=DAILY_LIFE_CHOICES, default=JOYFUL)
    focus_area = m.CharField(max_length=3, choices=FOCUS_AREA_CHOICES, default=STRESS)
    expectation = m.TextField()
    booking = m.ForeignKey(Booking, on_delete=m.CASCADE, related_name="assessment_booking", null=True)
    date_created = m.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.date_created)

class Invite(m.Model):
    """ Track invites """

    email = m.CharField(max_length=128)
    accepted = m.BooleanField()
    date_created = m.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email