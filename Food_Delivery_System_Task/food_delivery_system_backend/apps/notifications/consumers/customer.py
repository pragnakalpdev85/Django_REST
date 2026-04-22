import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import  database_sync_to_async

from apps.users.models import CustomerProfile


class CustomerConsumer(AsyncWebsocketConsumer):
    """
    Handles real-time notifications for a customer room.

    This consumer manages WebSocket connections, joins/leaves customer
    rooms, and broadcasts messages to all connected clients in the room.

    Attributes:
        room_name (str): The unique identifier for the customer room.
        room_group_name (str): The formatted group name used by Channels layer.
    """
    
    async def connect(self):    
        """Handles a new WebSocket connection requests"""
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            await self.close(code=4001)
            return

        self.customer_id = self.scope['url_route']['kwargs']['customer_id']
        self.room_group = f'customer_{self.customer_id}'

        if not await self.is_owner(user, self.customer_id):
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
        await self.send(text_data=json.dumps({'type': 'order_status_update', **event}))


    @database_sync_to_async
    def is_owner(self, user, customer_id):
        """Checks the user has access or not"""
        if user.role != 'customer':
            return False
        return CustomerProfile.objects.filter(id=customer_id, user=user).exists()