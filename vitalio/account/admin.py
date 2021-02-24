# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Forms
from .forms import AccountCreationForm, AccountChangeForm

# Models
from .models import Account, Profile, Address

class AccountAdmin(UserAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm
    model = Account
    list_display = ('email', 'is_staff', 'is_active', 'user_type')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class ProfileAdmin(admin.ModelAdmin):

    model = Profile

    list_display = ('account', 'first_name', 'last_name')
    list_filter = ('account', 'first_name', 'last_name',)
    
    search_fields = ('account',)
    ordering = ('account',)

class AddressAdmin(admin.ModelAdmin):

    model = Address

    list_display = ('profile',)
    list_filter = ('profile',)
    
    search_fields = ('profile',)
    ordering = ('profile',)

admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)