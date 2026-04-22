from rest_framework import serializers
from apps.restaurants.models import RestaurantProfile


class RestaurantInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for the RestaurantProfile model.
    
    Handles the conversion of RestaurantProfile instances to JSON and validates 
    incoming data for creating or updating Restaurant profile Returns only essential 
    informations about Restaurant like name, logo, address, average rating, total review
    and is open.
    """
    #additional fields
    is_open_now = serializers.SerializerMethodField()
    
    #Meta infomations
    class Meta:
        model = RestaurantProfile
        fields = [
            'id',
            'name',
            'description', 
            'address', 
            'logo', 
            'is_open_now', 
            'average_rating', 
            'total_reviews'
        ]
        
    def get_is_open_now(self, obj):
        """gets restaurant opening status"""
        return obj.is_currently_open()
    
    
