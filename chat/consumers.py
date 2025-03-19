import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, ChatRoom, User
from .encryption import encrypt_message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        user = self.scope['user']
        print(f"User connecting: {user}, Authenticated: {user.is_authenticated}")

        if not user.is_authenticated:
            print("User not authenticated, closing connection")
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f"WebSocket connected for user {user} in room {self.room_name}")

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f"WebSocket disconnected, close code: {close_code}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        if not user.is_authenticated:
            print("Received message from unauthenticated user, ignoring")
            return

        # Properly await the get_or_create result and get the first element
        room, created = await database_sync_to_async(ChatRoom.objects.get_or_create)(name=self.room_name)

        print(f"Received message from {user}: {message}")
        encrypted_message = encrypt_message(message, user.public_key)

        # Save the message to the database
        await database_sync_to_async(Message.objects.create)(
            room=room, user=user, content=encrypted_message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': encrypted_message,
                'username': user.username
            }
        )
        print(f"Sent encrypted message: {encrypted_message}")

    async def chat_message(self, event):
        print(f"Broadcasting message to client: {event['message']}")
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))