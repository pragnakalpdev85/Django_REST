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
    email = serializers.EmailField(source="user.email")
    phone_number = serializers.CharField(source="user.phone_number")
    avatar = serializers.ImageField(required=False, allow_null=True)
    
    #Meta informations
    class Meta:
        model = CustomerProfile
        fields = [
            'id',
            'email',
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
    
    def update(self, instance, validated_data):
        """Updates customer profile details"""
        
        full_name = self.initial_data.get("full_name", None)
        user_instance = instance.user

        if full_name is not None:
            name_parts = full_name.strip().split(" ", 1)
            user_instance.first_name = name_parts[0]
            user_instance.last_name = name_parts[1] if len(name_parts) > 1 else ""
            user_instance.save()

        user_data = validated_data.pop("user", None)
        print(user_data)
        if user_data:
            for attr, value in user_data.items():
                setattr(user_instance, attr, value)
            user_instance.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance