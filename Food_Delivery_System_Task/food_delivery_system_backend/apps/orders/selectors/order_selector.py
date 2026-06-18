from apps.orders.models import Order, Cart, OrderItem
from django.db.models import Count
from apps.common.utils.constants import DELIVERED, CANCELLED, RESTAURANT, CUSTOMER, DRIVER

class OrderCartSelector:
    """
    Order and Cart selector manages different queries for Order Cart models.
    """

    def get_order_queryset(user):
        """
        returns queryset for order model
        """
        if user.role == RESTAURANT:
            return (
                Order.objects
                .select_related('customer', 'restaurant', 'driver')
                .prefetch_related('order_menu')
                .annotate(items_count=Count('order_menu'))
                .filter(restaurant = user)
            )
        elif user.role == CUSTOMER:
            return (
                Order.objects
                .select_related('customer', 'restaurant', 'driver')
                .prefetch_related('order_menu')
                .annotate(items_count=Count('order_menu'))
                .filter(customer = user)
            )
        elif user.role == DRIVER:
            return (
                Order.objects
                .select_related('customer', 'restaurant', 'driver')
                .prefetch_related('order_menu')
                .annotate(items_count=Count('order_menu'))
                .filter(driver = user)
            )

        
    def get_active_orders(active):
        """
        Returns all the active orders
        """
        return (
            Order.objects.all()
            .select_related('customer', 'restaurant', 'driver')
            .prefetch_related('order_menu')
            .annotate(items_count=Count('order_menu'))
            .filter(status__in=active)
        )
        
    def get_history_orders():
        """
        Returns all the active orders
        """
        return (
            Order.objects.all()
            .select_related('customer', 'restaurant', 'driver')
            .prefetch_related('order_menu')
            .annotate(items_count=Count('order_menu'))
            .filter(status__in=[DELIVERED, CANCELLED])
        )
        
    def get_cart_by_customer(customer):
        """
        Returns cart of the customer
        """
        cart = (
            Cart.objects
            .filter(customer=customer)
            .prefetch_related('cart_menu')
            .first()
        )
        if not cart:
            cart = Cart.objects.create(customer=customer)
            
        return cart
        
    def get_empty_cart():
        """
        Returns empty queryset
        """
        return Cart.objects.none()
    
    def get_orderitems_of_cart(cart):
        """
        Returns all order items of cart
        """
        return (
            OrderItem.objects.all()
            .select_related('cart')
            .filter(cart = cart)
        )
        
        
        
        