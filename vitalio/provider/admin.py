# Django
from django.contrib import admin

# Models
from .models import Booking, Schedule, Provider

class BookingAdmin(admin.ModelAdmin):

    model = Booking

    list_display = ('patient', 'timeslot', 'isAccepted')
    list_filter = ('patient', )
    
    search_fields = ('patient',)
    ordering = ('patient',)

class ScheduleAdmin(admin.ModelAdmin):

    model = Schedule

    list_display = ('account', 'isBooked')
    list_filter = ('account', )
    
    search_fields = ('account',)
    ordering = ('account',)

class ProviderAdmin(admin.ModelAdmin):

    model = Provider

    list_display = ('profile', 'phone', 'years_of_experience', 'registered_council', 'electronic_card')
    list_filter = ('profile', 'years_of_experience', 'registered_council')
    
    search_fields = ('profile',)
    ordering = ('profile',)

admin.site.register(Booking, BookingAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Provider, ProviderAdmin)