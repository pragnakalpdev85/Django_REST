import json
import pytest
from django.test import TransactionTestCase
from channels.testing import WebsocketCommunicator
from rest_framework_simplejwt.tokens import RefreshToken
from asgiref.sync import sync_to_async

from food_delivery_system_backend.asgi import application
from apps.common.utils.constants import CONFIRMED, PREPARING, READY, DELIVERED
from apps.common.tests import (
    CustomerProfileFactory,
    DriverProfileFactory,
    RestaurantprofileFactory,
    OrderFactory
)


@pytest.mark.django_db
class TestCustomerConnection(TransactionTestCase):
    """
    Test suites for customer room.
    checks notification functionality in customer profile
    """
    
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.restaurant = RestaurantprofileFactory()
        self.owner_user = self.restaurant.owner
        
        self.customer = CustomerProfileFactory()
        self.customer_user = self.customer.user
        
        self.driver = DriverProfileFactory()
        self.driver_user = self.driver.user
        
        self.order = OrderFactory(customer=self.customer, restaurant=self.restaurant)
        
        self.refresh = RefreshToken.for_user(self.customer_user)
        self.access_token = str(self.refresh.access_token)

    async def test_order_status_change(self):
        """
        test to check the response after order status change
        """
        communicator = WebsocketCommunicator(application, f'/ws/customers/{self.customer.id}/?token={self.access_token}')
        response, _ = await communicator.connect()
        self.assertTrue(response)
        
        await self.change_order_status_to_preparing()
        response = await communicator.receive_from()
        response_data = json.loads(response)
        self.assertIn('type', response_data)
        
        await communicator.disconnect()

    async def test_order_status_change_ready(self):
        """
        test to check the response after changing order status to ready
        """
        communicator = WebsocketCommunicator(application, f'/ws/customers/{self.customer.id}/?token={self.access_token}')
        response, _ = await communicator.connect()
        self.assertTrue(response)
        
        await self.change_order_status_to_ready()
        response = await communicator.receive_from()
        response_data = json.loads(response)
        self.assertIn('type', response_data)
        
        await communicator.disconnect()

    async def test_order_status_change_delivered(self):
        """
        test to check response after order delivery
        """
        communicator = WebsocketCommunicator(application, f'/ws/customers/{self.customer.id}/?token={self.access_token}')
        response, _ = await communicator.connect()
        self.assertTrue(response)
        
        await self.change_order_status_to_delivered()
        response = await communicator.receive_from()
        response_data = json.loads(response)
        self.assertIn('type', response_data)
        
        await communicator.disconnect()

    @sync_to_async
    def change_order_status_to_preparing(self):
        self.order.status = PREPARING
        self.order.save()
        return True

    @sync_to_async
    def change_order_status_to_ready(self):
        self.order.status = READY
        self.order.save()
        return True

    @sync_to_async
    def change_order_status_to_delivered(self):
        self.order.status = DELIVERED
        self.order.save()
        return True