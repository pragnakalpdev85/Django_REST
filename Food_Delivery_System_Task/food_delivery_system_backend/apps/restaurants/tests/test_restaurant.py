import pytest
from uuid import uuid4
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.common.utils.constants import ITALIAN
from apps.restaurants.models import RestaurantProfile
from apps.common.tests import RestaurantprofileFactory


@pytest.mark.django_db
class TestRestaurant(APITestCase):
    """
    Test suite for restaurant profile and restaurants functionalities.
    
    Checks profile list, creation, profile update, profile data retrieval and profile delete operations
    restaurant menu retrieval, and retrieving active and popular restaurants.
    """
    
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.client = APIClient()
        self.restaurant = RestaurantprofileFactory()
        self.user = self.restaurant.owner
        
    def test_list_restaurants(self):
        """Tests restaurants list data is retrieved correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('restaurants-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RestaurantProfile.objects.count(),1)
        
    def test_retrieve_profile(self):
        """Tests restaurant profile data is retrieved correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('restaurants-detail', kwargs={'pk':self.restaurant.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RestaurantProfile.objects.count(),1)
        self.assertIn('restaurant_menuitem', response.data['data'])
        
    def test_profile_not_found(self):
        """Tests restaurant profile data not found works correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('restaurants-detail', kwargs={'pk': uuid4()})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_update_profile(self):
        """Tests restaurant profile upfate operations works correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('restaurants-detail', kwargs={'pk': self.restaurant.id})
        new_data = {
            "description": "new description",
            "cuisine_type": ITALIAN,
        }
        response = self.client.patch(url, data=new_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['description'], new_data['description'])
        self.assertEqual(response.data['data']['cuisine_type'], new_data['cuisine_type'])
        
    def test_delete_profile(self):
        """Tests customer profile data is deleted correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('restaurants-detail', kwargs={'pk': self.restaurant.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RestaurantProfile.objects.count(), 0)
        
    def test_list_menu_of_restaurant(self):
        """Tests listing menu items of the restaurant correctly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('restaurants-menu', kwargs={'pk': self.restaurant.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('restaurant_menuitem', response.data['data'])
        
    def test_list_popular_restaurants(self):
        """Tests listing 10 most popular restaurants based on average rating"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('restaurants-popular')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_list_active_restaurants(self):
        """Tests listing 10 most popular restaurants based on average rating"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('restaurants-active')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_list_owners_restaurants(self):
        """Tests listing owners all restaurant works correctly"""
        self.client.force_authenticate(user=self.user)
        url = reverse('restaurants-owner-restaurants')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)