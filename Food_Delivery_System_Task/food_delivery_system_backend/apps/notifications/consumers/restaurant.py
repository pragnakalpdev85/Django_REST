import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import  database_sync_to_async

from apps.restaurants.models import RestaurantProfile


class RestaurantConsumer(AsyncWebsocketConsumer):
    """
    Handles real-time notifications for a restaurant room.

    This consumer manages WebSocket connections, joins/leaves restaurant
    rooms, and broadcasts messages to all connected clients in the room.

    Attributes:
        room_name (str): The unique identifier for the restaurant room.
        room_group_name (str): The formatted group name used by Channels layer.
    """
    
    async def connect(self):
        """Handles a new WebSocket connection requests"""
        print('here')
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            await self.close(code=4001)
            return

        self.restaurant_id = self.scope['url_route']['kwargs']['restaurant_id']
        self.room_group = f'restaurant_{self.restaurant_id}'

        if not await self.is_owner(user, self.restaurant_id):
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
        
        print("hello")

    async def order_status_update(self, event):
        """sends message on order status update"""
        await self.send(text_data=json.dumps({'type': 'order_status_update', **event}))

    @database_sync_to_async
    def is_owner(self, user, restaurant_id):
        """Checks the user has access or not"""
        if user.role != 'restaurant_owner':
            return False
        return RestaurantProfile.objects.filter(id=restaurant_id, owner=user).exists()