# Django
from django.contrib import admin

# Models
from .models import Onboard

class OnboardAdmin(admin.ModelAdmin):

    model = Onboard

    list_display = ('account', 'isOnboarded')
    list_filter = ('account',)
    
    search_fields = ('account',)
    ordering = ('account',)

admin.site.register(Onboard, OnboardAdmin)
