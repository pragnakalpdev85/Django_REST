from rest_framework import serializers
from .orderitem import OrderItemSerializer
from apps.orders.models import Cart

class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.
    
    Handles the conversion of Order instances to JSON and validates 
    incoming data for creating or updating Cart.
    """
    
    cart_menu = OrderItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()
    final_total = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = [
            'id',
            'cart_menu', 
            'subtotal',
            'tax',
            'final_total',
            'item_count',
        ]
        read_only_fields=[
            'id'
        ]
    
    def get_item_count(self, obj):
        """Counts total order items in order"""
        return obj.cart_menu.count()
    
    def get_final_total(self, obj):
        """Ccalculates final total of the order"""
        return obj.calculate_total()