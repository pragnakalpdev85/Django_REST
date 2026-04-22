from rest_framework import serializers
from apps.users.models import CustomerProfile
from apps.common.utils.validators import validate_avatar_image


class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomerProfile model.
    
    Handles the conversion of CustomerProfile instances to JSON and validates 
    incoming data for creating or updating customer profile.
    """
    
    full_name = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)
    avatar = serializers.ImageField(required=False, allow_null=True)
    
    #Meta informations
    class Meta:
        model = CustomerProfile
        fields = [
            'id',
            'user_email',
            'phone_number',
            'full_name',
            'avatar', 
            'default_address',
            'saved_address', 
            'total_orders', 
            'loyalty_points',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'total_orders',
            'loyalty_points',
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
        
    