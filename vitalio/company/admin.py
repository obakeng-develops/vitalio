# Django
from django.contrib import admin

# Models
from .models import Company, Location, AccountCompany

admin.site.register(Company)
admin.site.register(Location)
admin.site.register(AccountCompany)