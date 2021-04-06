# Django
from django.contrib import admin

# Models
from .models import Assessment

class AssessmentAdmin(admin.ModelAdmin):

    model = Assessment

    list_display = ('date_created', 'feeling_today', 'daily_life_feeling', 'focus_area', 'booking')
    list_filter = ('date_created', 'feeling_today', 'daily_life_feeling', 'focus_area')
    
    search_fields = ('date_created', 'feeling_today', 'daily_life_feeling')
    ordering = ('date_created',)

admin.site.register(Assessment, AssessmentAdmin)
