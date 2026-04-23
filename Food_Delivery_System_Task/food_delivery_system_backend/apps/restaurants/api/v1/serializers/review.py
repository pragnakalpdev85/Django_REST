from rest_framework import serializers
from apps.restaurants.models import Review
from apps.common.utils.validators import validate_rating_points
from apps.users.api.v1.serializers import CustomerProfileSerializer


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    
    Handles the conversion of Review instances to JSON and validates 
    incoming data for creating or updating Review.
    """

    comment = serializers.CharField(min_length=5, max_length=1200)

    class Meta:
        model = Review
        fields = [
            'id', 
            'customer', 
            'restaurant', -
            'menu_item',
            'order', 
            'driver', 
            'rating', 
            'comment', 
            'created_at', 
            'updated_at',
        ]
        read_only_fields = [ 
            'created_at', 
            'updated_at'
        ]
    
    def validate_rating(self, value):
        """validates rating of review"""
        if value:
            validate_rating_points(value)
            
        return value