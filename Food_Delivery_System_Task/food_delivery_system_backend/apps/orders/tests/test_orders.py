import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from uuid import uuid4

from apps.orders.models import Order
from apps.common.utils.constants import PENDING, DELIVERED, CANCELLED, CONFIRMED
from apps.common.tests import (
    RestaurantprofileFactory,
    OrderItemFactory,
    OrderFactory,
    DriverProfileFactory,
    CustomerProfileFactory,
    MenuItemFactory
)


@pytest.mark.django_db
class TestOrder(APITestCase):
    """
    Test suite for order functionalities.
    
    Checks order list, creation, update, order data retrieval and order delete delete operations
    assign driver, place order,cancel order, update order status, list active orders and retrieving 
    order history functionalities.
    """
    
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.client = APIClient()
        
        self.restaurant = RestaurantprofileFactory()
        self.restaurant_owner = self.restaurant.owner
        
        self.driver = DriverProfileFactory()
        self.driver_user = self.driver.user
        
        self.customer = CustomerProfileFactory()
        self.customer_user = self.customer.user
        
        self.menu_item = MenuItemFactory(restaurant = self.restaurant)
        self.order = OrderFactory(restaurant = self.restaurant, customer = self.customer)
        self.order_items = OrderItemFactory(order = self.order, menu_item = self.menu_item)
        self.delivered_order = OrderFactory(restaurant = self.restaurant, customer = self.customer, status=DELIVERED)
     
    def test_create_order(self):
        """Tests order created correctly"""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders-list')
    
        response = self.client.post(
            url,
            data = {
                'order_menu': [
                    {
                        'menu_item': self.menu_item.id,
                        'quantity': 1,
                        'price': 200 
                    },
                ],
                'restaurant': self.restaurant.id,
                'customer': self.customer.id,
                'driver': None,
                'status': PENDING,
                'delivery_address': "new address"
            },
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_list_orders(self):
        """Tests order list retrieved correctly"""
        self.client.force_authenticate(user=self.restaurant_owner)
        url = reverse('orders-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_order(self):
        """Tests order retrieved correctly"""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders-detail', kwargs={'pk':self.order.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_order_not_found(self):
        """Tests order not found works correctly"""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders-detail', kwargs={'pk':uuid4()})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order(self):
        """Tests order deleted correctly"""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders-detail', kwargs={'pk':self.order.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_assign_driver(self):
        """Tests driver assigned correctly"""
        self.client.force_authenticate(user=self.restaurant_owner)
        url = reverse('orders-assign-driver', kwargs={'pk':self.order.id})
        response = self.client.post(
            url,
            data = {'driver_id': self.driver.id},
            format = 'json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['driver']['id'], str(self.driver.id))
        
    def test_cancel_order(self):
        """Tests order cancelled correctly"""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders-cancel', kwargs={'pk':self.order.id})
        response = self.client.post(
            url,
            data = None,
            format = 'json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['status'], CANCELLED)
        
    def test_cannot_cancel_order(self):
        """Tests order cancelation denied works correctly"""
        self.client.force_authenticate(user=self.customer_user)
        
        url = reverse('orders-cancel', kwargs={'pk':self.delivered_order.id})
        response = self.client.post(
            url,
            data = None,
            format = 'json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_order_status_update(self):
        """Tests order status updated correctly"""
        self.client.force_authenticate(user=self.restaurant_owner)
        
        url = reverse('orders-update-status', kwargs={'pk':self.order.id})
        response = self.client.post(
            url,
            data = {'status': CONFIRMED},
            format = 'json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['status'], CONFIRMED)
        
    def test_order_status_invalid_transition(self):
        """Tests invalid transition of the order status"""
        self.client.force_authenticate(user=self.restaurant_owner)
        url = reverse('orders-update-status', kwargs={'pk':self.delivered_order.id})
        response = self.client.post(
            url,
            data = {'status': CONFIRMED},
            format = 'json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_retrieve_active_orders(self):
        """Tests list of active order retrieved correctly"""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders-active')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_order_history(self):
        """Tests order histoery retrieved correctly"""
        self.client.force_authenticate(user=self.customer_user)
        
        url = reverse('orders-history')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)