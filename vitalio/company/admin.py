# Django
from django.contrib import admin

# Models
from .models import Company, Location, AccountCompany, Booking, CompanyBooking

class CompanyAdmin(admin.ModelAdmin):

    model = Company

    list_display = ('company_name', 'company_size')
    list_filter = ('company_name')
    
    search_fields = ('company_name',)
    ordering = ('company_name',)

class CompanyBookingAdmin(admin.ModelAdmin):

    model = CompanyBooking

    list_display = ('company', 'booking')
    list_filter = ('company',)
    
    search_fields = ('company',)
    ordering = ('cmopany',)


admin.site.register(Company)
admin.site.register(Location)
admin.site.register(AccountCompany)
admin.site.register(CompanyBooking)