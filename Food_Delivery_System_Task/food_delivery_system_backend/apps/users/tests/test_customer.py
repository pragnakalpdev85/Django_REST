import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from uuid import uuid4

from apps.users.models import CustomerProfile
from apps.common.tests import CustomerProfileFactory


@pytest.mark.django_db
class TestCustomer(APITestCase):
    """
    Test suite for customer profile functionalities.
    
    Checks profile creation, profile update, profile data retrieval and profile delete operations.
    """
    
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.client = APIClient()
        self.customer = CustomerProfileFactory()
        self.user = self.customer.user
    
    def test_retrieve_profile(self):
        """Tests customer profile data is retrieved correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('customers-detail', kwargs={'pk':self.customer.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_profile_not_found(self):
        """Tests customer proofile not found while retrieving customer profile"""
        self.client.force_authenticate(user=self.user)
        url = reverse('customers-detail', kwargs={'pk': uuid4()})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_update_profile(self):
        """Tests customer profile data is updated correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('customers-detail', kwargs={'pk': self.customer.id})
        new_data = {"default_address": "new address"}
        response = self.client.patch(url, new_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['default_address'], new_data['default_address'])
        
    def test_update_profile_validation(self):
        """Tests customer profile data is update data validation correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('customers-detail', kwargs={'pk': self.customer.id})
        new_data = {"default_address": {"new": "address"}}
        response = self.client.patch(url, new_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_profile(self):
        """Tests customer profile data is deleted correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('customers-detail', kwargs={'pk': self.customer.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomerProfile.objects.count(), 0)
        
        