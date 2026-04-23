from uuid import UUID
from apps.orders.models import OrderItem
from apps.restaurants.models import MenuItem
from apps.orders.api.v1.serializers import OrderItemCreateSerializer, CartSerializer
from apps.orders.selectors import OrderCartSelector
from apps.common.api.exceptions import DomainError, ErrorCodes


class CartService:
    """
    Handles logic for Orders.
    
    This service manages add to cart and remove from cart functionality.
    """
    
    def __init__(self, view_object, request_object):
        """
        Initializes service class object with view and request object
        """
        
        self.obj = view_object
        self.request = request_object
    

    def add_order_item_to_cart(self) -> dict:
        """
        Addes new order item to the cart
        
        Returns:
            dict: returns cart data in ReturnDict object
        """
        data = self.request.data
        serializer = OrderItemCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        new_item = OrderItem.objects.create(
            menu_item=MenuItem.objects.filter(id=data['menu_item']).first(),
            quantity=data['quantity'],
        )
    
        cart = self.obj.get_queryset().first()
        order_items = list(OrderCartSelector.get_orderitems_of_cart(cart))
        if new_item in order_items:
            idx = order_items.index(new_item)
            item = order_items[idx]
            item.quantity = new_item.quantity + item.quantity
        else: 
            order_items.append(new_item)
            
        cart.cart_menu.set(order_items) 
        cart_serializer = CartSerializer(cart)
        
        return cart_serializer.data
    
    def remove_order_item_from_cart(self) -> dict:
        """
        Removes order item from cart
        
        Returns:
            dict: returns cart data in ReturnDict object
        """
        data = self.request.data
        serializer = OrderItemCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        item = OrderItem.objects.filter(id = UUID(data['menu_item'])).first()
        
        if not item:
            raise DomainError(ErrorCodes.ORDER_ITEM_DOES_NOT_EXISTS)
        
        cart = self.obj.get_queryset().first()
        
        if not cart:
            raise DomainError(ErrorCodes.CART_DOES_NOT_EXISTS)
        
        order_items = OrderCartSelector.get_orderitems_of_cart(cart)
        queryset = order_items.exclude(id=item.id)
        order_items.filter(id=item.id).delete()

        cart.cart_menu.set(queryset) 
        cart_serializer = CartSerializer(cart)
        
        return cart_serializer.data