import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.orders.models import Cart, OrderItem
from apps.common.tests import (
    MenuItemFactory,
    OrderItemFactory,
    CustomerProfileFactory,
    RestaurantprofileFactory
)

@pytest.mark.django_db
class TestCart(APITestCase):
    """
    Test suite for Cart functionalities.
    
    Checks cart list, creation, retrieve, add item to cart, 
    remove item from cart and cart delete operations.
    """
    
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.client = APIClient()
        
        self.customer = CustomerProfileFactory()
        self.user = self.customer.user
        
        self.restaurant = RestaurantprofileFactory()
        self.restaurant_owner = self.restaurant.owner
        
        self.menu_item = MenuItemFactory(restaurant=self.restaurant)
        self.new_order_item = MenuItemFactory(restaurant=self.restaurant)
        
        self.cart = Cart.objects.create(customer=self.customer)
        self.order_item = OrderItemFactory(cart=self.cart, menu_item=self.menu_item, quantity=1, price=self.menu_item.price)
        
    def test_create_cart(self):
        """Tests cart created correctly"""
        self.client.force_authenticate(user=self.user)
        url = reverse('carts-list')
        response = self.client.post(
            url,
            data= {
                'order_menu': [
                    {'menu_item_id': self.menu_item.id, 'quantity': 1}
                ]
            },
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_cart(self):
        """Tests list cart retrieved correclty"""
        self.client.force_authenticate(user=self.user)
        url = reverse('carts-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_cart(self):
        """Tests cart retrieved correctly"""
        self.client.force_authenticate(user=self.user)
        url = reverse('carts-detail', kwargs={'pk': self.cart.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_add_to_cart(self):
        """Tests order item in cart is added correctly"""
        self.client.force_authenticate(user=self.user)
        url = reverse('carts-add-to-cart')
        response = self.client.post(
            url,
            data = {
                'menu_item': self.new_order_item.id, 
                'quantity': 1
            },
            format = 'json'
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OrderItem.objects.filter(cart=self.cart, menu_item=self.new_order_item).exists(), True)
        
    def test_remove_from_cart(self):
        """Tests orders item is removed from cart correctly"""
        self.client.force_authenticate(user=self.user)
        url = reverse('carts-remove-from-cart')
        response = self.client.post(
            url,
            data = {
                'menu_item': self.order_item.id, 
                'quantity': 1
            },
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OrderItem.objects.filter(id=self.order_item.id).exists(), False)
        
    def test_delete_cart(self):
        """Tests cart deleted correctly"""
        self.client.force_authenticate(user=self.user)
        url = reverse('carts-detail', kwargs={'pk': self.cart.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)