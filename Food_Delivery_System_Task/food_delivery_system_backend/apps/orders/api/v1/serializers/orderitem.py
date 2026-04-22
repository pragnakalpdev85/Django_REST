from rest_framework import serializers

from apps.orders.models import OrderItem
from apps.restaurants.api.v1.serializers import MenuItemSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.
    
    Handles the conversion of OrderItem instances to JSON and validates 
    incoming data for creating or updating OrderItem.
    """
    
    #additional relational fields
    menu_item = MenuItemSerializer(read_only=True)
    
    # additional computed fields
    total = serializers.SerializerMethodField()
    
    #Meta informations
    class Meta:
        model = OrderItem
        fields = [
            'order',
            'menu_item',
            'price', 
            'quantity', 
            'special_instructions',
            'total'
        ]
        
    def get_total(self, obj):
        """calculates total amount or orderitem price*quantitity"""
        return obj.calculate_total()