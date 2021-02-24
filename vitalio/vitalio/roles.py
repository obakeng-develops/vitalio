from rolepermissions.roles import AbstractUserRole

class Member(AbstractUserRole):
    available_permissions = {
        'create_booking': True,
        'update_booking': True,
    }

class Admin(AbstractUserRole):
    available_permissions = {
        'create_member': True,
        'update_member': True,
        'create_booking': True,
        'update_booking': True,
        'create_payment': True,
        'update_payment': True,
    }

class Provider(AbstractUserRole):
    available_permissions = {
        'create_booking': True,
        'update_booking': True,
        'create_schedule': True,
        'update_booking': True
    }