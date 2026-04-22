from apps.common.utils.constants import (
    CUSTOMER, DRIVER, RESTAURANT
)


class UserData:
    """
    UserData class contains dummy data for all user roles.
    """
        
    CUSTOMER_DATA = {
        "username": "testcustomer",
        "email": "customer@test.com",
        "phone_number": "+919998887776",
        "first_name": "Customer",
        "last_name": "Customer",
        "role": CUSTOMER,
        "password": "pass@1234",
        "password_confirm": "pass@1234",
    }
        
    DRIVER_DATA = {
        "username": "testdriver",
        "email": "driver@test.com",
        "phone_number": "+919998887776",
        "first_name": "Driver",
        "last_name": "Driver",
        "role": DRIVER,
        "password": "pass@1234",
        "password_confirm": "pass@1234",
    }
        
    OWNER_DATA = {
        "username": "testrestaurantowner",
        "email": "restaurantowner@test.com",
        "phone_number": "+919998887776",
        "first_name": "restaurantowner",
        "last_name": "restaurantowner",
        "role": RESTAURANT,
        "password": "pass@1234",
        "password_confirm": "pass@1234",
    }
    
    INVALID_EMAIL_DATA = {
        "username": "testrestaurantowner",
        "email": "wrong email",
        "phone_number": "+919998887776",
        "first_name": "restaurantowner",
        "last_name": "restaurantowner",
        "role": RESTAURANT,
        "password": "pass@1234",
        "password_confirm": "pass@1234",
    }
    
    INVALID_PHONE_DATA = {
        "username": "testrestaurantowner",
        "email": "restaurantowner@test.com",
        "phone_number": "wrong phone number",
        "first_name": "restaurantowner",
        "last_name": "restaurantowner",
        "role": RESTAURANT,
        "password": "pass@1234",
        "password_confirm": "pass@1234",
    }
    
    PASSWORD_MISMATCH_DATA = {
        "username": "testrestaurantowner",
        "email": "restaurantowner@test.com",
        "phone_number": "+919998887776",
        "first_name": "restaurantowner",
        "last_name": "restaurantowner",
        "role": RESTAURANT,
        "password": "pass@1234",
        "password_confirm": "wrong password",
    }