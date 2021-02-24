# Django
from django.db.models.signals import post_save
from django.dispatch import receiver

# Models
from .models import Account, Profile, Address
from onboard.models import Onboard

# Profile Signals
@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(account=instance)

# Address Signals
@receiver(post_save, sender=Profile)
def create_user_address(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(profile=instance)

# Onboard Signals
@receiver(post_save, sender=Account)
def create_user_onboard(sender, instance, created, **kwargs):
    if created:
        Onboard.objects.create(account=instance)

