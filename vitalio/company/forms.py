# Django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

# Models
from .models import Organization, Location

class OrganizationForm(ModelForm):

    class Meta:
        model = Organization
        fields = '__all__'
        exclude = ['members', 'subscription']

class OrganizationLocationForm(ModelForm):
    
    class Meta:
        model = Location
        fields = '__all__'
        exclude = ['organization']