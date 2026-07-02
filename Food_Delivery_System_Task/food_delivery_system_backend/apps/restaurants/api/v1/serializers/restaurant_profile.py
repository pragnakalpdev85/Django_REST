from rest_framework import serializers
from apps.restaurants.models import RestaurantProfile
from .restaurant_menuitem import RestaurantMenuItemSerializer
from apps.common.utils.validators import validate_avatar_image
from datetime import datetime


class RestaurantProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the RestaurantProfile model.
    
    Handles the conversion of RestaurantProfile instances to JSON and validates 
    incoming data for creating or updating RestaurantProfile.
    """
    #additional field from owner relationship 
    owner_name = serializers.CharField(source = 'owner.username')
    owner_email = serializers.CharField(source = 'owner.email')
    owner_phone_number = serializers.CharField(source = 'owner.phone_number')
    
    #additional fields
    is_open_now = serializers.SerializerMethodField(read_only=True)
    
    #nested menuitem serializer and item count field
    restaurant_menuitem = RestaurantMenuItemSerializer(many=True, read_only=True)
    item_count = serializers.IntegerField(read_only=True)                                                           
    
    #Meta informations:
    class Meta:
        model = RestaurantProfile
        fields = [
            'id',
            'owner_name', 
            'owner_email', 
            'owner_phone_number',
            'logo', 
            'banner', 
            'name', 
            'description', 
            'cuisine_type', 
            'address', 
            'opening_time',
            'closing_time',
            'is_open_now', 
            'delivery_fee',
            'minimum_order', 
            'average_rating',
            'total_reviews', 
            'item_count',
            'restaurant_menuitem',
        ]
        read_only_fields = [
            'id',
            'item_count',
            'total_reviews',
            'average_rating',
        ]
        
        
    def get_is_open_now(self, obj):
        """gets restaurant opening status"""
        return obj.is_currently_open()
    
class RestaurantCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for the RestaurantProfile model.
    
    Handles the conversion of RestaurantProfile instances to JSON and validates 
    incoming data for creating or updating RestaurantProfile.
    """
    
    class Meta:
        model = RestaurantProfile
        fields = [
            'id',
            'name',
            'address', 
            'description', 
            'cuisine_type', 
            'opening_time',
            'closing_time',
            'delivery_fee',
            'minimum_order',
        ]
        
    def validate_logo(self, value):
        """Validates logo image"""
        if value:
            validate_avatar_image(value, 5)
        return value
    
    def validate_banner(self, value):
        """Validates banner image"""
        if value:
            validate_avatar_image(value, 20)
        return value
    
    def validate_delivery_fee(self, value):
        """Validates Delivery fee if greater or equal to zero or not"""
        if value < 0:
            raise serializers.ValidationError("Delivery fee cannot be negative")
        return value
    
    def validate(self, data):
        """Validates request data"""
        if 'opening_time' in data and 'closing_time' in data:
            format = "%H:%M:%S"
            open_time = datetime.strptime(str(data['opening_time']), format)
            close_time = datetime.strptime(str(data['closing_time']), format)
            
            if close_time <= open_time:
                raise serializers.ValidationError("Closing time must be after Opening time")
        
        return super().validate(data)

    def create(self, validated_data):
        """Inject the owner from the request"""
        validated_data['owner'] = self.context['request'].user
        
        return super().create(validated_data=validated_data)