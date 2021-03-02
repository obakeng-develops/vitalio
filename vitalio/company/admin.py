# Django
from django.contrib import admin

# Models
from .models import Company, Location, AccountCompany, StripeCustomer

admin.site.register(Company)
admin.site.register(Location)
admin.site.register(AccountCompany)
admin.site.register(StripeCustomer)