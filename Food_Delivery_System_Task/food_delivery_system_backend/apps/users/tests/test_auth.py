import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.users.models import User, DriverProfile, CustomerProfile
from apps.restaurants.models import RestaurantProfile
from apps.common.tests import UserData

@pytest.mark.django_db
class TestAuth(APITestCase):
    """
    Test suite for the Authentication.
    
    Checks user registration with different roles, and user login.
    """
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.client = APIClient()
        self.customer_data = UserData.CUSTOMER_DATA
        self.driver_data = UserData.DRIVER_DATA
        self.owner_data = UserData.OWNER_DATA
        self.invalid_email = UserData.INVALID_EMAIL_DATA
        self.invalid_phone_number = UserData.INVALID_PHONE_DATA
        self.password_mismatch = UserData.PASSWORD_MISMATCH_DATA
        
    def test_customer_registration(self):
        """Tests user with customer role is created correctly"""
        url = reverse('register')
        response = self.client.post(url, self.customer_data, format="json")
        self.customer_profile_user = User.objects.filter(email=self.customer_data['email']).first()
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['email'] == self.customer_data["email"]
        assert 'tokens' in response.data
        
    def test_driver_registration(self):
        """Tests user with delivery driver role is created correctly"""
        url = reverse('register')
        response = self.client.post(url, self.driver_data, format="json")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["email"] == self.driver_data["email"]
        assert 'tokens' in response.data
        
    def test_owner_registration(self):
        """Tests user with restaurant owner role is created correctly"""
        url = reverse('register')
        response = self.client.post(url, self.owner_data, format="json")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["email"] == self.owner_data["email"]
        assert 'tokens' in response.data
        
    def test_invalid_email(self):
        """Tests registration of user with invalid email"""
        url = reverse('register')
        response = self.client.post(
            url, 
            self.invalid_email, 
            format="json"
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_invalid_phone_number(self):
        """Tests registration of user with invalid email"""
        url = reverse('register')
        response = self.client.post(
            url, 
            self.invalid_phone_number, 
            format="json"
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_password_mismatch(self):
        """Tests password and password_confirm fields mismatch"""
        url = reverse('register')
        response = self.client.post(
            url, 
            self.password_mismatch,
            format="json"
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        
    def test_login(self):
        """Tests user login works correctly with token generation"""
        #register user
        url = reverse('register')
        self.client.post(url, self.customer_data, format="json")
        
        #login user
        login_url = reverse('login')
        login_data = {
            'username': self.customer_data['username'],
            'password': self.customer_data['password'],
        }
        response = self.client.post(
            login_url,
            login_data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert 'tokens' in response.data
        
    def test_login_credentials(self):
        """Tests user login works correctly with invalid credentials"""
        #register user
        url = reverse('register')
        self.client.post(url, self.customer_data, format="json")
        
        #login user
        login_url = reverse('login')
        login_data = {
            'username': self.customer_data['username'],
            'password': 'Wrong credentials',
        }
        response = self.client.post(
            login_url,
            login_data,
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_profile_creation_customer(self):
        """Tests profile creation on user registration"""
        url = reverse('register')
        response = self.client.post(url, self.customer_data, format="json")
        
        user = User.objects.filter(email=self.customer_data['email']).first()
        customer = CustomerProfile.objects.filter(user = user).first()
        self.assertEqual(isinstance(customer, CustomerProfile), True)
        
    def test_profile_creation_driver(self):
        """Tests profile creation on user registration"""
        url = reverse('register')
        response = self.client.post(url, self.driver_data, format="json")
        
        user = User.objects.filter(email=self.driver_data['email']).first()
        driver = DriverProfile.objects.filter(user = user).first()
        self.assertEqual(isinstance(driver, DriverProfile), True)
    
    def test_profile_creation_restaurant(self):
        """Tests profile creation on user registration"""
        url = reverse('register')
        response = self.client.post(url, self.owner_data, format="json")
        
        user = User.objects.filter(email=self.owner_data['email']).first()
        restaurant = RestaurantProfile.objects.filter(owner = user).first()
        self.assertEqual(isinstance(restaurant, RestaurantProfile), True)
        
        
# async def test_customer_order_status_notification(self):

#     communicator = WebsocketCommunicator(application, f"/ws/customer/?token={self.customer_token}")
    
#     connected = await communicator.connect()
#     assert connected

#     response = await communicator.receive_json_from()
#     self.assertEqual(response['message'], "connected")
    
#     await assign_driver(self)
    
#     response = await communicator.receive_json_from(timeout=5)
    
#     self.assertEqual(response['data']['driver_name'], "driver")
#     self.assertEqual(response['data']['driver_vehicle_number'], "GJ-21-BB-3575")
#     self.assertEqual(response['data']['order_status'], "preparing")

#     await communicator.disconnect()


        