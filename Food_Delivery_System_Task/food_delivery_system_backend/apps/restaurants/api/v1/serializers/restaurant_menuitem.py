from rest_framework import serializers
from apps.restaurants.models import MenuItem


class RestaurantMenuItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the MenuItem model.
    
    Handles the conversion of MenuItem instances to JSON and validates 
    incoming data for creating or updating MenuItem.
    """
    
    #Meta informations
    class Meta:
        model = MenuItem
        fields = [
            'id',
            'name', 
            'price', 
            'is_available', 
            'image', 
            'average_rating',
            'category', 
            'dietary_info', 
            'total_reviews',
        ]
        read_only_fields = [
            'id',
            'total_reviews',
            'created_at',
            'updated_at',
        ]