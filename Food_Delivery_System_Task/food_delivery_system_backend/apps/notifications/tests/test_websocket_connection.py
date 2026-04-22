import pytest
from django.test import TransactionTestCase
from channels.testing import WebsocketCommunicator
from rest_framework_simplejwt.tokens import RefreshToken
from uuid import uuid4

from food_delivery_system_backend.asgi import application
from apps.common.utils.constants import CONFIRMED
from apps.common.tests import (
    OrderFactory,
    CustomerProfileFactory,
    DriverProfileFactory,
    RestaurantprofileFactory
)


@pytest.mark.django_db
class TestCustomerConnection(TransactionTestCase):
    """
    Test suites for cutomer room websocket connections.
    """
    
    def setUp(self):
        self.customer = CustomerProfileFactory()
        self.customer_user = self.customer.user
        self.refresh = RefreshToken.for_user(self.customer_user)
        self.access_token = str(self.refresh.access_token)

    async def test_consumer_connection(self):
        communicator = WebsocketCommunicator(application, f'/ws/customers/{self.customer.id}/?token={self.access_token}')
        response, _ = await communicator.connect()
        self.assertTrue(response)
        await communicator.disconnect()

    async def test_consumer_connection_without_token(self):
        communicator = WebsocketCommunicator(application, f'/ws/customers/{self.customer.id}/?token=')
        response, code = await communicator.connect()
        self.assertEqual(code, 4001)

    async def test_consumer_connection_invalid_id(self):
        communicator = WebsocketCommunicator(application, f'/ws/customers/{uuid4()}/?token={self.access_token}')
        response, code = await communicator.connect()
        self.assertEqual(code, 4003)

@pytest.mark.django_db
class TestDriverConnection(TransactionTestCase):
    """
    Test suites for driver room websocket connections.
    """
    
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.driver = DriverProfileFactory()
        self.driver_user = self.driver.user
        self.refresh = RefreshToken.for_user(self.driver_user)
        self.access_token = str(self.refresh.access_token)

    async def test_consumer_connection(self):
        """
        Tests driver room websocket connection
        """
        communicator = WebsocketCommunicator(application, f'/ws/drivers/{self.driver.id}/?token={self.access_token}')
        response, _ = await communicator.connect()
        self.assertTrue(response)
        await communicator.disconnect()

    async def test_consumer_connection_without_token(self):
        """
        Tests driver room websocket connection without token
        """
        communicator = WebsocketCommunicator(application, f'/ws/drivers/{self.driver.id}/?token=')
        response, code = await communicator.connect()
        self.assertEqual(code, 4001)

    async def test_consumer_connection_invalid_id(self):
        """
        Tests driver room websocket connection with invalid id
        """
        communicator = WebsocketCommunicator(application, f'/ws/drivers/{uuid4()}/?token={self.access_token}')
        response, code = await communicator.connect()
        self.assertEqual(code, 4003)

@pytest.mark.django_db
class TestRestaurantOwnerConnection(TransactionTestCase):
    """
    Test suites for restaurant room websocket connections.
    """
    
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.restaurant = RestaurantprofileFactory()
        self.owner_user = self.restaurant.owner
        self.refresh = RefreshToken.for_user(self.owner_user)
        self.access_token = str(self.refresh.access_token)

    async def test_consumer_connection(self):
        """
        Tests restaurant room websocket connection
        """
        communicator = WebsocketCommunicator(application, f'/ws/restaurants/{self.restaurant.id}/?token={self.access_token}')
        response, _ = await communicator.connect()
        self.assertTrue(response)
        await communicator.disconnect()

    async def test_consumer_connection_without_token(self):
        """
        Tests restaurant room websocket connection without jwt token
        """
        communicator = WebsocketCommunicator(application, f'/ws/restaurants/{self.restaurant.id}/?token=')
        response, code = await communicator.connect()
        self.assertEqual(code, 4001)

    async def test_consumer_connection_invalid_id(self):
        """
        Tests restaurant room websocket connection with invalid id of the restaurant
        """
        communicator = WebsocketCommunicator(application, f'/ws/restaurants/{uuid4()}/?token={self.access_token}')
        response, code = await communicator.connect()
        self.assertEqual(code, 4003)


@pytest.mark.django_db
class TestOrderRoomConnection(TransactionTestCase):
    """
    Test suites for order room websocket connections.
    """
    
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.restaurant = RestaurantprofileFactory()
        self.owner_user = self.restaurant.owner
        
        self.restaurant2 = RestaurantprofileFactory()
        self.owner_user2 = self.restaurant2.owner
        
        self.customer = CustomerProfileFactory()
        self.customer_user = self.customer.user
        
        self.customer2 = CustomerProfileFactory()
        self.customer_user2 = self.customer2.user
        
        self.driver = DriverProfileFactory()
        self.driver_user = self.driver.user
        
        self.driver2 = DriverProfileFactory()
        self.driver_user2 = self.driver2.user
        
        self.order = OrderFactory(customer=self.customer, driver=self.driver, restaurant=self.restaurant, status=CONFIRMED)
        
        self.refresh = RefreshToken.for_user(self.customer_user)
        self.access_token = str(self.refresh.access_token)

    async def test_customer_order_connection(self):
        """
        Tests order room websocket connection
        """        
        communicator = WebsocketCommunicator(application, f'/ws/orders/{self.order.id}/?token={self.access_token}')
        response, _ = await communicator.connect()
        self.assertTrue(response)
        await communicator.disconnect()

    async def test_owner_order_connection(self):
        """
        Tests order room websocket connection for restaurant owner
        """    
        refresh_token_for_owner = RefreshToken.for_user(self.owner_user)
        access_token = str(refresh_token_for_owner.access_token)
        communicator = WebsocketCommunicator(application, f'/ws/orders/{self.order.id}/?token={access_token}')
        response, _ = await communicator.connect()
        self.assertTrue(response)
        await communicator.disconnect()

    async def test_driver_order_connection(self):
        """
        Tests order room websocket connection for delivery driver
        """    
        refresh_token_for_driver = RefreshToken.for_user(self.driver_user)
        access_token = str(refresh_token_for_driver.access_token)
        communicator = WebsocketCommunicator(application, f'/ws/orders/{self.order.id}/?token={access_token}')
        response, _ = await communicator.connect()
        self.assertTrue(response)
        await communicator.disconnect()

    async def test_order_by_other_customer_connection(self):
        """
        Tests order room websocket connection for customer user
        """    
        refresh_token = RefreshToken.for_user(self.customer_user2)
        access_token = str(refresh_token.access_token)
        communicator = WebsocketCommunicator(application, f'/ws/orders/{self.order.id}/?token={access_token}')
        response, code = await communicator.connect()
        self.assertEqual(code, 4003)