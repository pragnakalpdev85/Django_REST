import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from uuid import uuid4

from apps.restaurants.models import MenuItem
from apps.common.tests import MenuItemFactory, RestaurantprofileFactory


@pytest.mark.django_db
class TestMenuItem(APITestCase):
    """
    Test suite for menu item functionalities.
    
    Checks menu item list, creation, menu item update, menu item data retrieval and menu item delete operations
    restaurant menu retrieval, and retrieving active and popular restaurants.
    """
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.client = APIClient()
        self.restaurant = RestaurantprofileFactory()
        self.user = self.restaurant.owner
        self.menu_item = MenuItemFactory.create(restaurant=self.restaurant)
    
    def test_menu_item_create_validation(self):
        """Tests menu item data validation while creating new menu item"""
        self.client.force_authenticate(user=self.user)
        url = reverse('menuitems-list')
        
        response = self.client.post(
            url, 
            data={
            'name': None,
            'description': 'menu item of restaurant',
            'price': 300,
            'is_available': True,
            'preparation_time': 20,
        }, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_list_all_menu_items(self):
        """Tests all menu items with restaurant data"""
        self.client.force_authenticate(user=self.user)
        url = reverse('menuitems-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_menu_item(self):
        """Tests menu item retrieved correctly"""
        self.client.force_authenticate(user=self.user)
        url = reverse('menuitems-detail', kwargs={'pk': self.menu_item.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('restaurant', response.data['data'])
        
    def test_update_menu_item(self):
        """Tests menu item updated correctly"""
        self.client.force_authenticate(user=self.user)
        url = reverse('menuitems-detail', kwargs={'pk': self.menu_item.id})
        new_data = {'price': 250}
        response = self.client.patch(url, data=new_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['data']['price']), new_data['price'])
        
    def test_update_data_validation(self):
        """Tests Menu Item data validation while update operation"""
        self.client.force_authenticate(user=self.user)
        url = reverse('menuitems-detail', kwargs={'pk': self.menu_item.id})
        new_data = {'price': "Hello"}
        response = self.client.patch(url, data=new_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_menu_item(self):
        """Tests menu item deleted correctly"""
        self.client.force_authenticate(user=self.user)
        url = reverse('menuitems-detail', kwargs={'pk': self.menu_item.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MenuItem.objects.count(), 0)
        
    def test_menu_item_not_found(self):
        """Tests Menu items not found"""
        self.client.force_authenticate(user=self.user)
        url = reverse('menuitems-detail', kwargs={'pk': uuid4()})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_toggle_availability_status(self):
        """Tests Menu Item availability toggles correctly"""
        self.client.force_authenticate(user=self.user)
        prev_availability_status = self.menu_item.is_available
        url = reverse('menuitems-toggle-availability', kwargs={'pk': self.menu_item.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['is_available'], not prev_availability_status)