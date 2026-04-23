from rest_framework import serializers

from apps.restaurants.models import RestaurantProfile, MenuItem

class OrderMenuItemSerializer(serializers.Serializer):
    """
    Input serializer for order menu.
    validates menu items price and quantity.
    """
    menu_item = serializers.UUIDField()
    quantity = serializers.IntegerField()
    
    def validate_quantity(self, value):
        """validates quantity or the order item"""
        if value <= 0:
            return serializers.ValidationError("Quantity must be greater than zero")

class OrderCreateSerializer(serializers.Serializer):
    """
    Input serializer for placing order.
    validates restaurant, minimum order, address required.
    """
    restaurant = serializers.UUIDField()
    delivery_address = serializers.CharField()
    special_instructions = serializers.CharField(required=False, allow_blank=True)
    order_menu = OrderMenuItemSerializer(many=True)
    

    def validate_order_menu(self, value):
        """
        Check at least one menu item is present.
        """
        if not value:
            raise serializers.ValidationError("At least one menu item is required.")
        return value

    def validate(self, attrs):
        """
        Validate minimum order amount and check menu items.
        """
        order_items = attrs.get('order_menu', [])
        restaurant_id = attrs.get('restaurant')

        if not restaurant_id:
            raise serializers.ValidationError("Restaurant is required.")
        try:
            restaurant = RestaurantProfile.objects.get(id=restaurant_id)
        except RestaurantProfile.DoesNotExist:
            raise serializers.ValidationError("Restaurant not found.")

        total = 0

        for item in order_items:
            menu_item_id = item.get('menu_item')
            quantity = item.get('quantity', 1)

            if not menu_item_id:
                raise serializers.ValidationError("Menu item is required.")
                
            try:
                menu_item = MenuItem.objects.get(id=menu_item_id)
            except MenuItem.DoesNotExist:
                raise serializers.ValidationError(f"Menu item {menu_item_id} not found.")
                
            if menu_item.restaurant != restaurant:
                raise serializers.ValidationError(f"Menu item {menu_item.name} does not belong to this restaurant.")

            total += menu_item.price * quantity

        if restaurant.minimum_order and total < restaurant.minimum_order:
            raise serializers.ValidationError(
                f"Minimum order amount is {restaurant.minimum_order}, your total is {total}."
            )

        # Store the instances in attrs so they can be used in create
        attrs['restaurant_instance'] = restaurant
        
        return attrs
    