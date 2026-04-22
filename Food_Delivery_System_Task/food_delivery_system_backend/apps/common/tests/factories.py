import factory #type: ignore
import uuid
from factory.django import DjangoModelFactory #type: ignore

from apps.users.models import User, CustomerProfile, DriverProfile
from apps.restaurants.models import MenuItem, RestaurantProfile
from apps.orders.models import Order, OrderItem, Cart
from apps.common.utils.constants import (
    CUSTOMER, 
    RESTAURANT, 
    DRIVER
)


class CustomerUserFactory(DjangoModelFactory):
    """
    Factory for generating User instances of role customer for testing.
    Generates only neccessory fields for model
    
    Fields:
        - username: user name field
        - email: generates fake email with username embeded in it.
        - role: CUSTOMER.
        - password: password field
        - first_name: first name of the user
        - last_name: last name of the user
        - phone_number: user contact number
    """
    id = factory.LazyFunction(uuid.uuid4)
    username = factory.Sequence(lambda n: f'customer_user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password=factory.django.Password('testpass123')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name') 
    role = CUSTOMER
    phone_number = '+919999999999'
    
    #meta informations
    class Meta:
        model = User
   
 
class RestaurantUserFactory(DjangoModelFactory):
    """
    Factory for generating User instances of role restaurant owner for testing.
    Generates only neccessory fields for model
    
    Fields:
        - username: user name field
        - email: generates fake email with username embeded in it.
        - role: RESTAURANT_OWNER.
        - password: password field
        - first_name: first name of the user
        - last_name: last name of the user
        - phone_number: user contact number
    """
    id = factory.LazyFunction(uuid.uuid4)
    username = factory.Sequence(lambda n: f'restaurant_user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password=factory.django.Password('testpass123')
    first_name = factory.Faker('first_name')    
    last_name = factory.Faker('last_name') 
    role = RESTAURANT
    phone_number = '+919999999999'
    
    #meta informations
    class Meta:
        model = User
        
    
class DriverUserFactory(DjangoModelFactory):
    """
    Factory for generating User instances of role delivery driver for testing.
    Generates only neccessory fields for model
    
    Fields:
        - username: user name field
        - email: generates fake email with username embeded in it.
        - role: DELIVERY_DRIVER.
        - password: password field
        - first_name: first name of the user
        - last_name: last name of the user
        - phone_number: user contact number
    """
    id = factory.LazyFunction(uuid.uuid4)
    username = factory.Sequence(lambda n: f'driver_user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password=factory.django.Password('testpass123')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name') 
    role = DRIVER
    phone_number = '+919999999999'
    
    #meta informations
    class Meta:
        model = User
    
    
class RestaurantprofileFactory(DjangoModelFactory):
    """
    Factory for generating restaurant profile instances for testing.
    Generates only required fields for model
    
    Fields:
        - owner: Subfactory for user with restaurant owner role
    """
    owner = factory.SubFactory(RestaurantUserFactory)
    
    class Meta:
        model = RestaurantProfile
        
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        owner = kwargs.pop('owner')
        profile = RestaurantProfile.objects.get(owner=owner)
        
        for key, value in kwargs.items():
            setattr(profile, key, value)
            
        profile.save()
        return profile
        
        
class CustomerProfileFactory(DjangoModelFactory):
    """
    Factory for generating customer profile instances for testing.
    Generates only required fields for model
    
    Fields:
        - user: Subfactory for user with customer role
    """
    user = factory.SubFactory(CustomerUserFactory)
    
    class Meta:
        model = CustomerProfile
        
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = kwargs.pop('user')
        profile = CustomerProfile.objects.get(user=user)
        
        for key, value in kwargs.items():
            setattr(profile, key, value)
            
        profile.save()
        return profile
        
    
class DriverProfileFactory(DjangoModelFactory):
    """
    Factory for generating driver profile instances for testing.
    Generates only required fields for model
    
    Fields:
        - user: Subfactory for user with restaurant owner role
    """
    user = factory.SubFactory(DriverUserFactory)
    
    class Meta:
        model = DriverProfile
        
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = kwargs.pop('user')
        profile = DriverProfile.objects.get(user=user)
        
        for key, value in kwargs.items():
            setattr(profile, key, value)
            
        profile.save()
        return profile
        

class MenuItemFactory(DjangoModelFactory):
    """
    Factory for generating menu item instances for testing.
    Generates only required fields for model
    
    Fields:
        - restaurant: Subfactory for user with restaurant owner role
        - name: name of the manu item
        - description: description for menu item
    """
        
    restaurant = factory.SubFactory(RestaurantprofileFactory)
    name = factory.Sequence(lambda n: f'menuitem{n}')
    description = factory.Sequence(lambda n: f'menuitem{n}')
    price = 300
    
    #meta informations
    class Meta:
        model = MenuItem
    
    
class OrderFactory(DjangoModelFactory):
    """
    Factory for generating order instances for testing.
    Generates only required fields for model
    
    Fields:
        - restaurant: Subfactory for user with restaurant owner role
        - customer: Subfactory for user with customer role
    """
        
    restaurant = factory.SubFactory(RestaurantprofileFactory)
    customer = factory.SubFactory(CustomerProfileFactory)
    
    #meta infromations
    class Meta:
        model = Order
        
        
class CartFactory(DjangoModelFactory):
    """
    Factory for generating cart instances for testing.
    Generates only required fields for model
    
    Fields:
        - customer: Subfactory for customer profile
    """
    customer = factory.SubFactory(CustomerProfileFactory)
    
    #meta informations
    class Meta:
        model = Cart
            
 
class OrderItemFactory(DjangoModelFactory):
    """
    Factory for generating order item instances for testing.
    Generates only required fields for model
    
    Fields:
        - order: Subfactory order 
    """
    order = factory.SubFactory(OrderFactory)
    menu_item = factory.SubFactory(MenuItemFactory)
    cart = factory.SubFactory(CartFactory)
       
    #meta informations 
    class Meta:
        model = OrderItem
