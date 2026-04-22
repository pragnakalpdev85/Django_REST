from django.utils import timezone
from django.shortcuts import get_object_or_404

from apps.users.models import DriverProfile
from apps.orders.models import OrderItem, Order
from apps.orders.selectors import OrderCartSelector
from apps.restaurants.models import MenuItem
from apps.common.api.exceptions import DomainError, ErrorCodes
from apps.orders.api.v1.serializers import OrderItemCreateSerializer, OrderSerializer
from apps.common.utils.constants import (
    PENDING, CONFIRMED, CANCELLED, READY, PICKEDUP, PREPARING, DELIVERED
)


class OrderService():
    """
    Handles logic for Orders.
    
    This service manages create, list, update, delete, retrieve, updtate status,
    assign driver, cancel order, retrieve order history and retrieve active orders
    operations of order functionality.
    """
    
    def __init__(self, view_object, request_object):
        """
        Initializes service class object with view and request object
        """
        
        self.obj = view_object
        self.request = request_object
        
    def create_order(self):
        """
        Creates new order
        """
        data = self.request.data
        serializer = self.obj.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        customer = self.request.user.customer
        restaurant = validated_data['restaurant_instance']
        delivery_address = validated_data['delivery_address']
        special_instructions = validated_data.get('special_instructions', '')
        order_items_data = validated_data['order_menu']
        
        order = Order.objects.create(
            customer=customer,
            restaurant=restaurant,
            delivery_address=delivery_address,
            special_instructions=special_instructions,
            status=PENDING
        )
        
        for item_data in order_items_data:
            menu_item = MenuItem.objects.get(id=item_data['menu_item'])
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item_data.get('quantity', 1),
                special_instructions=item_data.get('special_instructions', '')
            )
            
        order.calculate_total()
        order.save()
        
        serializer = OrderSerializer(order)
        return serializer.data
    
    def update_order(self, partial_flag):
        """
        Updates order partially or whole order
        """
        order = self.obj.get_object()
        data = self.request.data.get('order_menu')

        if data is not None:
            order_items = OrderItemCreateSerializer(data=data, many=True)
            order_items.is_valid(raise_exception=True)

            from apps.restaurants.models import MenuItem
            from rest_framework.exceptions import ValidationError

            # Validate menu items
            for item_data in order_items.validated_data:
                menu_item_id = item_data['menu_item']
                try:
                    menu_item = MenuItem.objects.get(id=menu_item_id)
                except MenuItem.DoesNotExist:
                    raise ValidationError({"order_menu": f"Menu item {menu_item_id} not found."})
                
                if menu_item.restaurant != order.restaurant:
                    raise ValidationError({"order_menu": f"Menu item does not belong to this restaurant."})

        serializer = self.obj.get_serializer(
            order,
            data=self.request.data,
            partial=partial_flag
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if data is not None:
            order.order_menu.all().delete()
            for item_data in order_items.validated_data:
                menu_item = MenuItem.objects.get(id=item_data['menu_item'])
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=item_data.get('quantity', 1),
                    special_instructions=item_data.get('special_instructions', '')
                )
        
        return self.obj.get_serializer(order).data
    
    def retrieve_order(self):
        """
        retrieve order by id
        """
        order = self.obj.get_object()
        serializer = self.obj.get_serializer(order)
        
        return serializer.data
    
    def list_orders(self):
        """
        Lists all orders
        """
        queryset = self.obj.filter_queryset(self.obj.get_queryset())
        page = self.obj.paginate_queryset(queryset)
        if page is not None:
            serializer = self.obj.get_serializer(page, many=True)
            return self.obj.get_paginated_response(serializer.data).data

        serializer = self.obj.get_serializer(queryset, many=True)
        return serializer.data
    
    def assign_driver_to_order(self):
        """
        Assignes driver to an order
        """
        
        order = self.obj.get_object()
        driver_id = self.request.data.get('driver_id')
        driver = get_object_or_404(
            DriverProfile, id = driver_id
        )
        
        if not driver.is_available:
            raise DomainError(ErrorCodes.DRIVER_NOT_AVAILABLE)
            
        order.driver = driver
        order.save()
        serializer = self.obj.get_serializer(order)
        return serializer.data
    
    def cancel_order(self):
        """
        Cancel order
        """
        order = self.obj.get_object()
        if not order.can_cancel():
            raise DomainError(ErrorCodes.CANNOT_CANCEL_ORDER)
        order.status = 'cancelled'
        order.save(update_fields=['status', 'updated_at'])
        
        serializer = self.obj.get_serializer(order)
        return serializer.data
    
    def update_order_status(self):
        """
        Updates status of the perticular order
        """
        order = self.obj.get_object()
        VALID_TRANSITIONS = {
            PENDING:   [CONFIRMED, CANCELLED],
            CONFIRMED: [PREPARING, CANCELLED],
            PREPARING: [READY],
            READY:     [PICKEDUP],
            PICKEDUP: [DELIVERED],
        }
        
        new_status = self.request.data.get('status')
        allowed = VALID_TRANSITIONS.get(order.status, [])
        if new_status not in allowed:
            raise DomainError(ErrorCodes.CANNOT_UPDATE_ORDER_STATUS)
        
        order.status = new_status
        if new_status == DELIVERED:
            order.actual_delivery_time = timezone.now()
        
        if 'estimated_delivery_time' in self.request.data:
            order.estimated_delivery_time = self.request.data['estimated_delivery_time']
            
        order.save(update_fields=['status', 'actual_delivery_time','estimated_delivery_time', 'updated_at'])
        serializer = self.obj.get_serializer(order)
        
        return serializer.data
    
    def list_active_orders(self):
        """
        Lists all active orders 
        """
        active = [PENDING, CONFIRMED, PREPARING, READY, PICKEDUP]
        queryset = OrderCartSelector.get_active_orders(active)
        serializer = self.obj.get_serializer(queryset, many=True)
        
        return serializer.data
    
    def list_history_of_orders(self):
        """
        Lists all cancelled or delivered orders
        """
        queryset = OrderCartSelector.get_history_orders()
        serializer = self.obj.get_serializer(queryset, many=True)
        return serializer.data
        
        