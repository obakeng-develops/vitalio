# Django
from django.contrib import admin

# Models
from .models import Assessment, Invite

class AssessmentAdmin(admin.ModelAdmin):

    model = Assessment

    list_display = ('date_created', 'feeling_today', 'daily_life_feeling', 'focus_area', 'booking')
    list_filter = ('date_created', 'feeling_today', 'daily_life_feeling', 'focus_area')
    
    search_fields = ('date_created', 'feeling_today', 'daily_life_feeling')
    ordering = ('date_created',)


class InviteAdmin(admin.ModelAdmin):
    
    model = Invite

    list_display = ('email', 'accepted', 'date_created')
    list_filter = ('email', 'accepted',)
    
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Invite, InviteAdmin)