# Django
from django.db import models as m

# Models
from account.models import Account, Subscription
from provider.models import Booking

class Organization(m.Model):
    """ An organization or company """

    organization_name = m.CharField(max_length=50, blank=False)
    members = m.ManyToManyField(Account, related_name="organizations", through="Membership")
    subscription = m.ForeignKey(Subscription, null=True, blank=True, on_delete=m.SET_NULL, help_text="The organization's subscription, if it exists.")

    def __str__(self):
        return self.organization_name

class Membership(m.Model):
    """ A user's organization membership """

    organization = m.ForeignKey(Organization, on_delete=m.CASCADE)
    user = m.ForeignKey(Account, on_delete=m.CASCADE)

    def __str__(self):
        return self.user.email

class Location(m.Model):
    """ Organization's location """

    organization = m.ForeignKey(Organization, on_delete=m.CASCADE, related_name="organization_address", default="")
    line_one = m.CharField(max_length=50, blank=True, null=True)
    surburb = m.CharField(max_length=50, blank=True, null=True)
    city = m.CharField(max_length=50, blank=True, null=True)
    province = m.CharField(max_length=20, blank=True, null=True)
    country = m.CharField(max_length=50, blank=True, null=True)
    zip_code = m.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.line_one + ", " + self.surburb + ", " + self.city + ", " + self.province + ", " + self.country + ", " + self.zip_code

class CompanyBooking(m.Model):
    company = m.ForeignKey(Organization, on_delete=m.CASCADE, related_name="company_bookings")
    booking = m.ForeignKey(Booking, on_delete=m.CASCADE, related_name="bookings_made_by_company")

    def __str__(self):
        return str(self.company) + " (" + str(self.booking) + ")"
