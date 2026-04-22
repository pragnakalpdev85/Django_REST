from rest_framework import serializers
from apps.users.models import DriverProfile
from apps.common.utils.validators import validate_avatar_image


class DriverProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the DriverProfile model.
    
    Handles the conversion of DriverProfile instances to JSON and validates 
    incoming data for creating or updating DriverProfile.
    """
    
    full_name = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)
    avatar = serializers.ImageField(required=False, allow_null=True)
    
    #Meta informations:
    class Meta:
        model = DriverProfile
        fields = [
            'id',
            'full_name',
            'user_email',
            'phone_number',
            'avatar', 
            'is_available', 
            'total_deliveries', 
            'total_reviews',
            'average_rating', 
            'vehicle_type',
            'vehicle_number', 
            'license_number',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'total_deliveries',
            'total_reviews',
            'average_rating',
            'created_at',
            'updated_at',
        ]
        
    def get_full_name(self, obj):
        """Returns the user's full name."""
        return f"{obj.user.first_name} {obj.user.last_name}".strip()
    
    def validate_avatar(self, value):
        """Avatar image"""
        if value:
            validate_avatar_image(value, 5)
        return value