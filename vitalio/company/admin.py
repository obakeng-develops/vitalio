# Django
from django.contrib import admin

# Models
from .models import Organization, Membership, Location, CompanyBooking

class OrganizationAdmin(admin.ModelAdmin):

    model = Organization

    list_display = ('organization_name', 'subscription',)
    list_filter = ('organization_name',)
    
    search_fields = ('organization_name',)
    ordering = ('organization_name',)

class CompanyBookingAdmin(admin.ModelAdmin):

    model = CompanyBooking

    list_display = ('company', 'booking')
    list_filter = ('company',)
    
    search_fields = ('company',)
    ordering = ('company',)

class MembershipAdmin(admin.ModelAdmin):
    
    model = Membership

    list_display = ('organization', 'user')
    list_filter = ('organization',)
    
    search_fields = ('organization',)
    ordering = ('organization',)


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(CompanyBooking, CompanyBookingAdmin)