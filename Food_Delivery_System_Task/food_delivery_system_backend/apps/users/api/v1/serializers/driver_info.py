from rest_framework import serializers
from apps.users.models import DriverProfile
from apps.common.utils.validators import validate_avatar_image


class DriverInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for the DriverProfile model with only assential informations.
    
    Handles the conversion of DriverProfile instances to JSON and validates 
    incoming data for creating or updating DriverProfile.
    """
    #additional fields from user
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
            'total_reviews',
            'average_rating',
        ]
        
    def get_full_name(self, obj):
        """Returns the user's full name."""
        return f"{obj.user.first_name} {obj.user.last_name}".strip()
    
    def validate_avatar(self, value):
        """validates image"""
        if value:
            validate_avatar_image(value, 5)
        
        return value