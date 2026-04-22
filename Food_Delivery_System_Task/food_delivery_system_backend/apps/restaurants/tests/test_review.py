import pytest
from uuid import uuid4
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.restaurants.models import Review
from apps.common.tests import (
    MenuItemFactory, 
    RestaurantprofileFactory, 
    OrderFactory,
    DriverProfileFactory,
    CustomerProfileFactory,
)

@pytest.mark.django_db
class TestReview(APITestCase):
    """
    Test suite for restaurant profile and restaurants functionalities.
    
    Checks profile list, creation, profile update, profile data retrieval and profile delete operations
    restaurant menu retrieval, and retrieving active and popular restaurants.
    """
    
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.client = APIClient()
        self.user_profile = CustomerProfileFactory()
        self.user = self.user_profile.user
        self.restaurant = RestaurantprofileFactory()
        self.restaurant_user = self.restaurant.owner
        self.driver = DriverProfileFactory()
        self.driver_user = self.driver.user
        self.menu_item = MenuItemFactory(restaurant = self.restaurant)
        
    def test_create_restaurant_review(self):
        """Tests review created for restaurant corretlly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('reviews-list')
        response = self.client.post(
            url, 
            data = {
                'customer': self.user_profile.id,
                'restaurant': self.restaurant.id,
                'rating': 4,
                'comment': 'new comment',
            },
            format = 'json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_menu_item_review(self):
        """Tests review created for driver correctlly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('reviews-list')
        response = self.client.post(
            url,
            data = {
                'customer': self.user_profile.id,
                'menu_item': self.menu_item.id,
                'rating': 4,
                'comment': 'new comment'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
          
    def test_create_driver_review(self):
        """Tests review created for driver correctlly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('reviews-list')
        response = self.client.post(
            url,
            data = {
                'customer': self.user_profile.id,
                'driver': self.driver.id,
                'rating': 4,
                'comment': 'new comment'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_invalid_rating(self):
        """Tests invalid rating in rating creation"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('reviews-list')
        response = self.client.post(
            url,
            data = {
                'driver': self.driver.id,
                'rating': 10,
                'comment': 'new comment',
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_restaurant_review(self):
        """Tests listing review of restaurant correctlly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('restaurants-reviews', kwargs={'pk': self.restaurant.id})
        response = self.client.get(url)
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_list_driver_review(self):
        """Tests listing review of driver correctlly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('drivers-reviews', kwargs={'pk': self.driver.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_list_menu_item_review(self):
        """Tests listing review of menu_item correctlly"""
        
        self.client.force_authenticate(user=self.user)
        url = reverse('menuitems-reviews', kwargs={'pk': self.menu_item.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_not_found(self):
        """Tests review not found while retrieving"""
        self.client.force_authenticate(user=self.user)
        url = reverse('menuitems-reviews', kwargs={'pk': uuid4()})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_retrieve_review(self):
        """Tests review retrieved correctlly"""
        self.review = Review.objects.create(
            customer=self.user_profile, 
            driver = self.driver, 
            rating = 4, 
            comment = "new comment"
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('reviews-detail', kwargs={'pk': self.review.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_review(self):
        """Tests review updated correctlly"""
        self.review = Review.objects.create(
            customer=self.user_profile, 
            driver = self.driver, 
            rating = 4, 
            comment = "new comment"
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('reviews-detail', kwargs={'pk': self.review.id})
        new_comment = 'updated comment'
        response = self.client.patch(
            url,
            data = {'comment': new_comment},
            format = 'json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['comment'], new_comment)
        
    def test_delete_review(self):
        """Tests review deleted correctly"""
        self.review = Review.objects.create(
            customer=self.user_profile, 
            driver = self.driver, 
            rating = 4, 
            comment = "new comment"
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('reviews-detail', kwargs={'pk': self.review.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)
        
