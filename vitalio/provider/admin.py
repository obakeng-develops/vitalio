# Django
from django.contrib import admin

# Models
from .models import Booking, Schedule

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

admin.site.register(Booking, BookingAdmin)
admin.site.register(Schedule, ScheduleAdmin)