from rest_framework import serializers

class OrderItemCreateSerializer(serializers.Serializer):
    """
    Input data serilizer for a single order item when placing an order.
    Does not map to model directly used in OrderCreateSerilizer.validate()
    """
    
    menu_item = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, required=False)
    special_instructions = serializers.CharField(required=False, allow_blank=True)