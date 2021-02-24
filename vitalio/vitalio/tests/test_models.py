# Django
from django.test import TestCase
from datetime import datetime
from django.utils import timezone

# Models
from account.models import Account, Profile, Address
from company.models import Company, Location, AccountCompany
from onboard.models import Onboard
from provider.models import Schedule, Booking

class TestModels(TestCase):
    def test_account_has_profile(self):
        account = Account.objects.create_user(email='foo@bar.com', password='test123abc', user_type='1')
        profile = Profile.objects.get(account=account)
        
        self.assertEqual(account, profile.account)

    def test_profile_has_address(self):
        account = Account.objects.create_user(email='foo@bar.com', password='test123abc', user_type='1')
        profile = Profile.objects.get(account=account)
        address = Address.objects.get(profile=profile)
        
        self.assertEqual(profile, address.profile)

    def test_company_has_location(self):
        company = Company.objects.create(company_name='Vitalio', company_size='10')
        location = Location.objects.create(company=company, line_one='123 Test Str', surburb='Northriding', city='Randburg', province='Gauteng', country='South Africa', zip_code='0216')

        self.assertEqual(company, location.company)

    def test_account_has_company(self):
        account = Account.objects.create_user(email='foo@bar.com', password='test123abc', user_type='1')
        company = Company.objects.create(company_name='Vitalio', company_size='10')
        account_company = AccountCompany.objects.create(company=company, user=account)
        
        self.assertTrue(account)
        self.assertTrue(company)
        self.assertTrue(account_company)
    
    def test_account_has_onboard(self):
        account = Account.objects.create_user(email='foo@bar.com', password='test123abc', user_type='1')
        onboard = Onboard.objects.get(account=account)

        self.assertEqual(account, onboard.account)

    def test_schedule_created(self):
        # Come back to this
        pass

    def test_booking_created(self):
        # Come back to this
        pass

    def test_account_model_str(self):
        account = Account.objects.create_user(email='foo@bar.com', password='test123abc', user_type='1')
        self.assertEqual(str(account), "foo@bar.com")

    def test_profile_model_str(self):
        account = Account.objects.create_user(email='foo@bar.com', password='test123abc', user_type='1')
        profile = Profile.objects.get(account=account)
        profile.first_name = 'Foo'
        profile.last_name = 'Doe'

        self.assertEqual(str(profile), "Foo Doe")

    def test_account_model_str(self):
        account = Account.objects.create_user(email='foo@bar.com', password='test123abc', user_type='1')
        profile = Profile.objects.get(account=account)
        profile.first_name = 'Foo'
        profile.last_name = 'Doe'
        address = Address.objects.get(profile=profile)
        address.line_one = '12 Test str'
        address.surburb = 'Northriding'
        address.city = 'Randburg'
        address.province = 'Gauteng'
        address.zip_code = '0216'
        address.country = 'South Africa'

        self.assertEqual(str(address), "12 Test str, Northriding, Randburg, Gauteng, South Africa, 0216")

    def test_company_model_str(self):
        company = Company.objects.create(company_name='Vitalio', company_size='10')

        self.assertEqual(str(company), "Vitalio")

    def test_location_model_str(self):
        company = Company.objects.create(company_name='Vitalio', company_size='10')
        location = location = Location.objects.create(company=company, line_one='123 Test Str', surburb='Northriding', city='Randburg', province='Gauteng', country='South Africa', zip_code='0216')

        self.assertEqual(str(location), "123 Test Str, Northriding, Randburg, Gauteng, South Africa, 0216")

    def test_account_company_model_str(self):
        account = Account.objects.create_user(email='foo@bar.com', password='test123abc', user_type='1')
        company = Company.objects.create(company_name='Vitalio', company_size='10')
        account_company = AccountCompany.objects.create(company=company, user=account)

        self.assertEqual(str(account_company), account.email + " from " + company.company_name)

    def test_onboard_model_str(self):
        account = Account.objects.create_user(email='foo@bar.com', password='test123abc', user_type='1')
        onboard = Onboard.objects.get(account=account)

        self.assertEqual(str(onboard), "False")

    def test_schedule_model_str(self):
        # Come back to this
        pass
    
    def test_booking_model_str(self):
        # Come back to this
        pass
