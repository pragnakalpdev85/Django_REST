from django.db import models
from django.utils import timezone
from django.db.models import Avg

from apps.common.models import DateTimeStamped, UUIDModel, AVGRating
from apps.common.utils.constants import (
    ITALIAN, INDIAN, CHINESE, MEDITERRANEAN,
    MEXICAN, JAPANESE, THAI, AMERICAN,
    APPETIZER, MAINCOURSE, DESSERT, BEVERAGE, SIDEDISH,
    VEGITERIAN, VEGAN, GLUTENFREE, DAIRYFREE, NONE
)


class RestaurantProfile(UUIDModel, DateTimeStamped, AVGRating):
    """
    RestaurantProfile model that provides fields user(onetoone realationship), name,
    description, cuisine_type(choices), address, opening_time, closing_time, is_open,
    media fields like logo and banner image fields, delivery_fee, minimum_order, 
    average_rating, total_reviews, created_at and updated_at.
    """
    
    #choices for cuisines
    CUISINES = (
        (ITALIAN, 'Italian'),
        (CHINESE, 'Chinese'),
        (INDIAN, 'Indian'),
        (MEXICAN, 'Mexican'),
        (AMERICAN, 'American'),
        (JAPANESE, 'Japanese'),
        (THAI, 'Thai'),
        (MEDITERRANEAN, 'Mediterranean')
    )
    
    #user id field with OneToOne relationship with User model
    owner = models.OneToOneField(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='restaurant_owner'
    ) 
    
    #basic fields
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    cuisine_type = models.CharField(max_length=20, choices=CUISINES, default=INDIAN)
    address = models.TextField()
    
    #media fields
    logo = models.ImageField(upload_to='restaurant_logo_images/', blank=True, null=True)
    banner = models.ImageField(upload_to='restaurant_banner_images/', blank=True, null=True)
    
    #restaurant timing
    opening_time = models.TimeField(null=True)
    closing_time = models.TimeField(null=True)
    is_open = models.BooleanField(default=False)    
    
    #other fields
    delivery_fee = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    minimum_order = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    
    average_rating = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    total_reviews = models.IntegerField(default=0)
    
    #meta informations
    class Meta:
        db_table = 'restaurant_profiles'
        indexes = [
            models.Index(fields=['-created_at'], name='newest_restaurant_idx')
        ]
    
    #additional methods
    def is_currently_open(self):
        """Returns restaurants opening status"""
        
        if self.opening_time and self.closing_time:
            self.is_open = True if timezone.now().time() <= self.closing_time and timezone.now().time() > self.opening_time else False
        return self.is_open
    
    def update_average_rating(self):
        return super().update_average_rating(self.restaurant_review.all())
    
    
class MenuItem(UUIDModel, DateTimeStamped, AVGRating):
    """
    MenuItem model that prvides fields name, description, price, image, is_available,
    category, dietary_info of the item.
    Model represents Food items restaurant serves.
    """
    
    #category choices
    CATEGORY = (
        (APPETIZER, 'Appetizer'),
        (MAINCOURSE, 'Main Course'),
        (DESSERT, 'Dessert'),
        (BEVERAGE, 'Beverage'),
        (SIDEDISH, 'Side Dish')
    )
    
    #dietary information choices
    DIETARY_INFO = (
        (VEGITERIAN, 'Vegetarian'),
        (VEGAN, 'Vegan'),
        (GLUTENFREE, 'Gluten-Free'),
        (DAIRYFREE, 'Dairy-Free'),
        (NONE, 'None')
    )
    
    #foreign key to restaurant
    restaurant = models.ForeignKey(
        RestaurantProfile, 
        on_delete=models.CASCADE, 
        related_name='restaurant_menuitem'
    )
    
    #Item details
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    is_available = models.BooleanField(default=True)
    preparation_time = models.IntegerField(default=0)
    
    #Item image
    image = models.ImageField(upload_to='menuitem_images/',blank=True,null=True)
    
    #types of Item
    category = models.CharField(max_length=20, choices=CATEGORY, default=APPETIZER)
    dietary_info = models.CharField(max_length=20, choices=DIETARY_INFO, default=NONE)
    
    #Meta informations
    class Meta:
        db_table = 'menu_items'
        indexes = [
            models.Index(fields=['-created_at'], name='newest_menuitem_idx'),
            models.Index(fields=['restaurant'], name='restaurant_menuitem_idx')
        ]
        
    def update_average_rating(self):
        """Updates average rating of menu item"""
        return super().update_average_rating(self.menuitem_reviews.all())
    
        

class Review(UUIDModel, DateTimeStamped):
    """
    Review model provides fields customer, restaurant, menu_item, order, rating, 
    comment, created_at, and updated_at
    """
    
    #entities related to review model
    customer = models.ForeignKey(
        'users.CustomerProfile', 
        on_delete=models.CASCADE, 
        related_name='customer_review'
    )
    restaurant = models.ForeignKey(
        RestaurantProfile, 
        on_delete=models.CASCADE, 
        related_name='restaurant_review', 
        null=True, 
        blank=True
    )
    menu_item = models.ForeignKey(
        MenuItem, 
        on_delete=models.CASCADE, 
        related_name='menuitem_reviews', 
        null=True, 
        blank=True
    )
    order = models.ForeignKey(
        'orders.Order', 
        on_delete=models.CASCADE, 
        related_name='order_review', 
        null=True, 
        blank=True
    )
    driver = models.ForeignKey(
        'users.DriverProfile', 
        on_delete=models.CASCADE, 
        related_name='driver_review', 
        null=True, 
        blank=True
    )
    
    #rating and comment fields
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    
    #meta informations
    class Meta:
        db_table = 'reviews'
        indexes = [
            models.Index(fields=['-created_at'], name='newest_review_idx'),
            models.Index(fields=['restaurant'], name='restaurant_review_idx'),
            models.Index(fields=['customer'], name='customer_review_idx'),
        ]    