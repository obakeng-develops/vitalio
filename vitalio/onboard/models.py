# Django
from django.db import models as m

# Models
from account.models import Account

class Onboard(m.Model):
    account = m.ForeignKey(Account, on_delete=m.CASCADE, related_name="onboarding_account")
    isOnboarded = m.BooleanField(default=False)

    def __str__(self):
        return str(self.isOnboarded)