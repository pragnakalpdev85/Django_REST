import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from uuid import UUID

from apps.users.models import DriverProfile
from apps.common.tests import RestaurantUserFactory, DriverProfileFactory


@pytest.mark.django_db
class TestDriver(APITestCase):
    """
    Test suite for driver profile and drivers list functionalities.
    
    Checks profile creation, profile update, profile data retrieval, profile delete operations,
    driver availability status toggle, and retrieving data of all active drivers.
    """
    
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.client = APIClient()
        self.driver = DriverProfileFactory()
        self.user = self.driver.user
        self.restaurant = RestaurantUserFactory()
        
    def test_list_driver_required_auth(self):
        """Tests listing drivers requires authentication"""
        url = reverse('drivers-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_driver_profile(self):
        """Tests Driver data list is retrieved correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('drivers-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_profile(self):
        """Tests Driver profile data is retrieved correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('drivers-detail', kwargs={'pk':self.driver.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UUID(response.data["data"]['id']), self.driver.id)
        
    def test_update_profile(self):
        """Tests driver profile data is update data validation correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('drivers-detail', kwargs={'pk':self.driver.id})
        new_data = {'vehicle_number': 'GJ-21 9812'}
        response = self.client.patch(url, data=new_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]['vehicle_number'], new_data['vehicle_number'])
        
    def test_data_validation(self):
        """Tests data validation while updating driver profile"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('drivers-detail', kwargs={'pk':self.driver.id})
        new_data = {
            'vehicle_number': None,
            'vehicle_type': None,
            'license_number': None
        }
        response = self.client.patch(url, data=new_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_profile(self):
        """Tests driver profile deleted correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('drivers-detail', kwargs={'pk':self.driver.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DriverProfile.objects.count(), 0)
        
    def test_active_driver_list(self):
        """Tests list of active driver retrieved correctly"""
        
        self.client.force_authenticate(user=self.restaurant)
        url = reverse('drivers-active')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
          
    def test_activity_status_toggle(self):
        """Tests activity status toggle of driver"""
        
        self.client.force_authenticate(user=self.user)
        current_status = self.driver.is_available
        url = reverse('drivers-toggle-availability', kwargs={'pk':self.driver.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['is_available'],not current_status)