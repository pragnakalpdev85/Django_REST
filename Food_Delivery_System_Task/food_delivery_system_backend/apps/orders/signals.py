from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from ..common.utils.constants import (
    DELIVERED
)


@receiver([post_save], sender='orders.OrderItem')
def recalculate_order_total(sender, instance, **kwargs):
    """
    Signal handler to automatically calculate total amount after saving/deleting an order item.
    
    Triggerd by the 'post_save' and 'post_delete' signals on the OrderItem Model. Ensures every orders total
    amount is calculated after saving an OrderItem.
    
    Args:
        sender (Model): Model class that sent the signal
        instance (OrderItem): instance of the 'OrderItem' being saved/deleted
        **kwargs : Additional keyword argument passed by the signal dispatcher
    """
    
    if instance.order:
        instance.order.calculate_total()
        instance.order.save(update_fields=['subtotal', 'total_amount', 'delivery_fee'])

        
@receiver(post_save, sender='orders.Order')
def handle_order_saved(sender, instance, created, **kwards):
    """
    Signal handler to automatically notify and update users stats after saving the order
    
    Triggerd by the 'post_save' signal on the Order Model. Ensures every entity related
    to order will get notified when order is created or order status is updated and     
    changes customer and driver stats when order is delivered
    
    Args:
        sender (Model): Model class that sent the signal
        instance (Order): instance of the 'Order' being saved
        created (bool): true if new record was created else false
        **kwargs : Additional keyword argument passed by the signal dispatcher
    """
    
    if created:
        notify_restaurant_for_order(instance)
    else:
        notify_order_status_change(instance)
        
        if instance.status == DELIVERED:
            update_delivery_status(instance)
            
            
def notify_restaurant_for_order(order):
    """
    Helper function for handling order place notifications
    
    Used to send message of order created to the restaurant with order_number,
    customer_name, order_total, and order_status
    
    Args:
        order (Order): instance of order class
    """
    #get channel layer
    channel_layer = get_channel_layer()
    if not channel_layer:
        return
    
    try:
        # async_to_sync safely runs the group_send coroutine
        async_to_sync(channel_layer.group_send)(
            f'restaurant_{order.restaurant.id}',
            {
                'type': 'new_order',
                'order_number': order.order_number,
                'customer_name': order.customer.user.username,
                'status': order.status,
            }
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    
def notify_order_status_change(order):
    """
    Helper function for handling notification on order status change
    
    Used to send message of order status is changed to the restaurant, 
    customer, order, and driver
    
    Args:
        order (Order): instance of order class
    """
    #get channel layer
    channel_layer = get_channel_layer()
    if not channel_layer:
        return
    
    #message structure
    msg_payload = {
        'type': 'order_status_update',
        'order_number': order.order_number,
        'status': order.status,
        'estimated_delivery_time': order.estimated_delivery_time,
    }
    
    #rooms to send message
    rooms = [
        f'order_{order.id}',
        f'customer_{order.customer.id}',
        f'restaurant_{order.restaurant.id}'
    ]
    
    #add driver if present
    if order.driver:
        rooms.append(f'driver_{order.driver.id}')
       
    #sends message 
    for room in rooms:
        async_to_sync(channel_layer.group_send)(room, msg_payload)
        

def update_delivery_status(order):
    """
    Helper function for handling stats update of customer and driver
    
    Used to update total_order and loyalty point of customer and update total delivery
    of driver
    
    Args:
        order (Order): instance of order class
    """
    #updates customer stats
    customer = order.customer
    customer.total_orders += 1
    customer.loyalty_points += 10
    customer.save(update_fields = ['total_orders', 'loyalty_points', 'updated_at'])
    
    #update driver stats
    if order.driver:
        driver = order.driver
        driver.total_deliveries += 1
        driver.save(update_fields = ['total_deliveries', 'updated_at'])