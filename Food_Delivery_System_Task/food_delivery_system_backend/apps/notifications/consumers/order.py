import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import  database_sync_to_async

from apps.orders.models import Order


class OrderConsumer(AsyncWebsocketConsumer):
    """
    Handles real-time order notifications for a order room.

    This consumer manages WebSocket connections, joins/leaves order
    rooms, and broadcasts messages to all connected clients in the room.

    Attributes:
        room_name (str): The unique identifier for the order room.
        room_group_name (str): The formatted group name used by Channels layer.
    """

    async def connect(self):
        """Handles a new WebSocket connection requests"""
        
        #checks if user is authenticated or not
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            await self.close(code=4001)
            
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        print(self.order_id)
        self.room_group = f'order_{self.order_id}'
    
        if not await self.has_access(user, self.order_id):
            await self.close(code=4003)
            return
            
        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()
        
    async def disconnect(self, code):
        """Handles closing event of websocket connection"""
        
        if hasattr(self, 'room_group'):
            await self.channel_layer.group_discard(self.room_group, self.channel_name)
            
    async def new_order(self, event):
        """Sends message on new order creation"""
        await self.send(text_data=json.dumps({
            'type': 'new_order',
            'order_number': event['order_number'],
            'customer_name': event['customer_name'],
            'status': event['status'],
        }))
        
    async def order_status_update(self, event):
        """sends message on order status update"""
        await self.send(text_data=json.dumps({
            'type': 'order_status_update',
            'order_number': event['order_number'],
            'status': event['status'],
            'estimated_delivery_time': event.get('estimated_delivery_time'),
        }))
        
    @database_sync_to_async
    def has_access(self, user, order_id):
        """Checks the user has access or not"""
        try:
            order = Order.objects.select_related(
                'restaurant__owner', 'customer__user', 'driver__user'
            ).get(id=order_id)
            
            return (
                order.customer.user == user
                or order.restaurant.owner == user 
                or (order.driver and order.driver.user == user)
            )
        except Order.DoesNotExist:
            return False