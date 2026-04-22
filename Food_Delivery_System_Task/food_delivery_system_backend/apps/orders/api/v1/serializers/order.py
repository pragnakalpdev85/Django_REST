from rest_framework import serializers

from apps.orders.models import Order
from apps.restaurants.api.v1.serializers import RestaurantInfoSerializer
from apps.users.api.v1.serializers import DriverProfileSerializer, CustomerProfileSerializer
from .orderitem import OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    
    Handles the conversion of Order instances to JSON and validates 
    incoming data for creating or updating Order.
    """
    
    #additional relational fields data
    restaurant = RestaurantInfoSerializer(read_only=True)
    customer = CustomerProfileSerializer(read_only=True)
    driver = DriverProfileSerializer(read_only=True)
    order_menu = OrderItemSerializer(many=True, read_only=True)
    
    # additional computed field
    can_review = serializers.SerializerMethodField()
    can_cancel = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    final_total = serializers.SerializerMethodField()
    estimated_delivery_time = serializers.SerializerMethodField()
    
    #Meta informations
    class Meta:
        model = Order
        fields = [
            'order_menu', 
            'restaurant', 
            'customer', 
            'driver', 
            'order_number',
            'status', 
            'delivery_address', 
            'special_instructions', 
            'subtotal',
            'tax', 
            'estimated_delivery_time', 
            'actual_delivery_time',
            'can_cancel',
            'can_review',
            'final_total',
            'item_count',
        ]
        
    def get_can_review(self, obj):
        """User is permited to review or not"""
        #if order is delivered than user can review the order
        return obj.is_delivered()
    
    def get_can_cancel(self, obj):
        """Permitted to cancel order or not"""
        return obj.can_cancel()
    
    def get_item_count(self, obj):
        """Counts total order items in order"""
        return obj.order_menu.count()
    
    def get_final_total(self, obj):
        """Ccalculates final total of the order"""
        return obj.calculate_total()
    
    def get_estimated_delivery_time(self, obj):
        """Calculates estimated delivery time"""
        return obj.calculate_estimated_time()

    