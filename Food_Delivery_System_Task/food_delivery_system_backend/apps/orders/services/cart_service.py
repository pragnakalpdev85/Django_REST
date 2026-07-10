from rest_framework.exceptions import ValidationError

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
    
        cart = self.obj.get_queryset()
        order_items = list(OrderCartSelector.get_orderitems_of_cart(cart))
        
        if order_items:
            first_order_item = order_items[0]
            print("="*100)
            print(first_order_item.menu_item.restaurant.id, MenuItem.objects.filter(id=data['menu_item']).first().restaurant.id)
            if first_order_item.menu_item.restaurant.id != MenuItem.objects.filter(id=data['menu_item']).first().restaurant.id:
                raise ValidationError(
                    "All menu items should be from one restaurant only"
                )

        quantity_increament = False
        for order_item in order_items:
            if order_item.menu_item == new_item.menu_item:
                order_item.quantity += new_item.quantity
                order_item.save()
                quantity_increament = True
                break
        if quantity_increament == False:
            order_items.append(new_item)
        
        cart.cart_menu.set(order_items)
        cart.save()
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
        
        cart = self.obj.get_queryset()
        order_items = OrderCartSelector.get_orderitems_of_cart(cart)
        quantity_decreament = False
        for order_item in order_items:
            if str(order_item.menu_item.id) == str(serializer.data["menu_item"]):
                print( serializer.data["quantity"] == 1,  serializer.data["quantity"])
                if order_item.quantity == 1:
                    order_items = order_items.exclude(id=order_item.id)
                    order_items.filter(id=order_item.id).delete()
                    quantity_decreament = True
                else:
                    order_item.quantity -= int(serializer.data["quantity"])
                    order_item.save()
                    quantity_decreament = True
                break
            
        if quantity_decreament == False:
            raise DomainError(ErrorCodes.ORDER_ITEM_DOES_NOT_EXISTS)
        
        cart.cart_menu.set(order_items) 
        cart_serializer = CartSerializer(cart)
        return cart_serializer.data