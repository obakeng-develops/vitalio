# Django
from django.db import models as m

# Models
from account.models import Account
from provider.models import Booking

class Company(m.Model):
    company_name = m.CharField(max_length=50, blank=False)
    company_size = m.IntegerField()

    def __str__(self):
        return self.company_name

class Location(m.Model):
    company = m.ForeignKey(Company, on_delete=m.CASCADE, related_name="company_address")
    line_one = m.CharField(max_length=50, blank=True, null=True)
    surburb = m.CharField(max_length=50, blank=True, null=True)
    city = m.CharField(max_length=50, blank=True, null=True)
    province = m.CharField(max_length=20, blank=True, null=True)
    country = m.CharField(max_length=50, blank=True, null=True)
    zip_code = m.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.line_one + ", " + self.surburb + ", " + self.city + ", " + self.province + ", " + self.country + ", " + self.zip_code

class AccountCompany(m.Model):
    company = m.ForeignKey(Company, on_delete=m.CASCADE, related_name="company_account")
    user = m.ForeignKey(Account, on_delete=m.CASCADE, related_name="user_company")

    def __str__(self):
        return self.user.email + " from " + self.company.company_name

class CompanyBooking(m.Model):
    company = m.ForeignKey(Company, on_delete=m.CASCADE, related_name="company_bookings")
    booking = m.ForeignKey(Booking, on_delete=m.CASCADE, related_name="bookings_made_by_company")

    def __str__(self):
        return str(self.company) + " (" + str(self.booking) + ")"
