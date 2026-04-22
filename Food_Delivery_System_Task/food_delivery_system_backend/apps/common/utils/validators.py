import re
from rest_framework import serializers

def validate_avatar_image(value, max_file_size):
    """Validates avatar image checks format and file size"""
    max_size = max_file_size * 1024 * 1024  # 10MB
    if value.size > max_size:
        raise serializers.ValidationError("File size cannot exceed 10MB")
    
    allowed_types = ['jpg', 'jpeg', 'png']
    file_ext = value.name.split('.')[-1].lower()
    if file_ext not in allowed_types:
        raise serializers.ValidationError(f"File type not allowed. Allowed: {allowed_types}")
    
    return value  

def validate_phone_number_format(value):
    """validates phone number format"""
    # Basic regex for format validation
    if not re.match(r'^\+?1?\d{9,15}$', value):
        raise serializers.ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    return value      
    
def validate_positive_price(value):
    """Validates price is not less than zero"""
    if value <= 0:
        raise serializers.ValidationError("Price must be a positive value")
    
def validate_rating_points(value):
    """Validates rating is integer and inbetween 1 to 5"""
    if not (1 <= value <= 5):
        raise serializers.ValidationError("Rating must be between 1 and 5")