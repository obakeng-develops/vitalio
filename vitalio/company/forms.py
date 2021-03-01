# Django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

# Models
from .models import Company

class CompanyForm(ModelForm):

    class Meta:
        model = Company
        fields = '__all__'