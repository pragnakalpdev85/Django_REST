from rest_framework import serializers
from apps.restaurants.models import MenuItem
from .restaurant_info import RestaurantInfoSerializer
from apps.common.utils.validators import validate_avatar_image, validate_positive_price


class MenuItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the MenuItem model with restaurant.
    
    Handles the conversion of MenuItem instances to JSON and validates 
    incoming data for creating or updating MenuItem.
    """
    
    #nested restaurant serializer
    restaurant = RestaurantInfoSerializer()
    
    #Meta informations
    class Meta:
        model = MenuItem
        fields = [
            'restaurant', 
            'name', 
            'description',
            'price', 
            'is_available', 
            'image', 
            'average_rating', 
            'category', 
            'dietary_info', 
            'total_reviews' 
        ]
        
class MenuItemCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for the MenuItem model with restaurant.
    
    Handles the conversion of MenuItem instances to JSON and validates 
    incoming data for creating or updating MenuItem.
    """
    
    class Meta:
        model = MenuItem
        fields = [
            'id',
            'restaurant',
            'name',
            'description',
            'price',
            'is_available',
            'preparation_time',
            'image',
            'category',
            'dietary_info',
        ]
        read_only_fields = ['id']
        
    def validate_price(self, value):
        """Validates price of the menu item"""
        if value:
            validate_positive_price(value)
        return value
    
    def validate_image(self, value):
        """Validates image of the menu item"""
        if value:
            validate_avatar_image(value, 5)
        return value