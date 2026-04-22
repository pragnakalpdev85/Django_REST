from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from apps.common.models import DateTimeStamped, UUIDModel, AVGRating
from apps.common.utils.constants import (
    DRIVER, CUSTOMER, RESTAURANT,
    BIKE, SCOOTER, CAR
)


class User(AbstractUser, UUIDModel, DateTimeStamped):
    """
    User model that extends AbstractUser model and TimeStamped model.
    model Provides extra fields role, phone_number, created_at and updated_at.  
    """
    
    #role choices
    ROLE = (
        (CUSTOMER, 'Customer'),
        (RESTAURANT, 'Restaurant Owner'),
        (DRIVER, 'Delivery Driver')
    )
    
    #additional fields
    role = models.CharField(max_length=25, choices=ROLE, default=CUSTOMER)
    phone_number = models.CharField(max_length=15)

    #removing some unnecessary fields
    date_joined = None
    
    groups = models.ManyToManyField(
        Group,
        related_name="user_groups",  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_permissions",
        blank=True,
    )

    #Meta infromations
    class Meta:
        db_table = 'users'

    #functions for checking roles
    def is_customer(self):
        """Checks User is customer ot not"""
        return self.role == CUSTOMER
    
    def is_restaurant_owner(self):
        """Checks User is restaurant owner ot not"""
        return self.role == RESTAURANT
    
    def is_delivery_driver(self):
        """Checks User is driver ot not"""
        return self.role == DRIVER
    

class CustomerProfile(UUIDModel, DateTimeStamped):
    """
    CustomerProfile model that provides fields user(onetoone realationship), avatar(image), 
    default_address, saved_address, total_orders, loyalty_points, created_at, and updated_at.
    """
    
    #user id field with OneToOne relationship with User model
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='customer'
    )
    
    #basic fields
    avatar = models.ImageField(upload_to='customer_profile_images/', blank=True, null=True)
    default_address = models.TextField(blank=True, null=True)
    saved_address = models.JSONField(default=list, blank=True)
    total_orders = models.IntegerField(default=0)
    loyalty_points = models.IntegerField(default=0)
    
    #meta informations
    class Meta:
        db_table = 'customer_profiles'


class DriverProfile(UUIDModel, DateTimeStamped, AVGRating):
    """
    DriverProfile model that provides fields user(onetoone realationship), avatar(image), 
    is_available, total_delivery, average_rating, created_at, and updated_at, and vehicle and 
    other driver details like vehicle_type, vehicle_number, license_number.
    """
    
    #choice for vehicle types
    VEHICLE_TYPE = (
        (BIKE, 'Bike'),
        (SCOOTER, 'Scooter'),
        (CAR, 'Car')
    )
    
    #user id field with OneToOne relationship with User model
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='driver'
    )
    
    #basic fields
    avatar = models.ImageField(upload_to='driver_profile_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    total_deliveries = models.IntegerField(default=0)
    
    #vehicle details
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE, default=BIKE)
    vehicle_number = models.CharField(max_length=25)
    license_number = models.CharField(max_length=25)
    
    #meta informations
    class Meta:
        db_table = 'driver_profiles'
        indexes = [
            models.Index(fields=['-created_at'], name='newest_driver_idx')
        ]
    
    def update_availability(self):
        """Updates availibility status of driver"""
        self.is_available = not self.is_available
        self.save(update_fields=['is_available', 'updated_at'])
        
    def update_averge_rating(self):
        """Updates average rating of rating"""
        return super().update_averge_rating(self.driver_review.all())
        
    def get_delivery_stats(self):
        """Returns dilivery stats of the driver"""
        return {
            'total_delivery': self.total_deliveries,
            'total_reviews': self.total_reviews,
            'average_rating': self.average_rating,
            'is_available': self.is_available,
        }