from rest_framework import serializers
from apps.users.models import User
from apps.common.utils.validators import validate_phone_number_format


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for the Custom User model.
    
    Handles the conversion of CustomUser instances to JSON and validates 
    incoming data for creating or updating custom users.
    """
    
    #additional fields
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(max_length = 15)
    
    #Meta informations
    class Meta:
        model = User
        fields = [
            'id',
            'username',  
            'first_name', 
            'last_name', 
            'email', 
            'role', 
            'phone_number',
            'is_active', 
            'password', 
            'password_confirm', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]
        
    #validates password and custom password fields
    def validate(self, data):
        """validates password and confirm password match"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        
        return data
    
    def validate_phone_number(self, value):
        """validates phone number format"""
        # Basic regex for format validation
        return validate_phone_number_format(value)

    #creates CustomUser Object
    def create(self, validated_data):
        """creates new user model instance"""
        validated_data.pop('password_confirm') 
        password = validated_data.pop('password')  
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
