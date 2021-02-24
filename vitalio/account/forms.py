# Django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

# Models
from .models import Account, Profile


class AccountCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Account
        fields = ('email',)


class AccountChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ('email',)

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['profile_image', 'profile_slug', 'random_id', 'account']
