# Django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

# Models
from .models import Account, Profile, Subscription, Address


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

class SubscriptionForm(ModelForm):
    
    class Meta:
        model = Subscription
        fields = '__all__'
        exclude = ['start_date', 'status', 'subscription_owner']

class AddressForm(ModelForm):
    
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['profile']
