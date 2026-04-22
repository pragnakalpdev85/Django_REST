import json
import pytest
from django.test import TransactionTestCase
from channels.testing import WebsocketCommunicator
from rest_framework_simplejwt.tokens import RefreshToken
from asgiref.sync import sync_to_async

from food_delivery_system_backend.asgi import application
from apps.common.tests import (
    CustomerProfileFactory,
    DriverProfileFactory,
    RestaurantprofileFactory,
    OrderFactory
)
from apps.common.utils.constants import CONFIRMED, PREPARING


@pytest.mark.django_db
class TestDriverConnection(TransactionTestCase):
    """
    Test suites for driver room.
    checks notification functionality in driver profile
    """
    
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.restaurant = RestaurantprofileFactory()
        self.owner_user = self.restaurant.owner
        
        self.customer = CustomerProfileFactory()
        self.customer_user = self.customer.user
        
        self.driver = DriverProfileFactory()
        self.driver_user = self.driver.user
        
        self.order = OrderFactory(customer=self.customer, driver=self.driver, restaurant=self.restaurant, status=CONFIRMED)
        
        self.refresh = RefreshToken.for_user(self.driver_user)
        self.access_token = str(self.refresh.access_token)

    async def test_order_status_change(self):
        """
        test to check the response after order status change
        """
        communicator = WebsocketCommunicator(application, f'/ws/drivers/{self.driver.id}/?token={self.access_token}')
        response, _ = await communicator.connect()
        self.assertTrue(response)
        
        await self.change_order_status_to_preparing()
        response = await communicator.receive_from()
        response_data = json.loads(response)
        self.assertIn('type', response_data)
        
        await communicator.disconnect()

    @sync_to_async
    def change_order_status_to_preparing(self):
        self.order.status = PREPARING
        self.order.save()
        return True