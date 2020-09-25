import json
from django.core.serializers.json import DjangoJSONEncoder
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import asyncio
from datetime import datetime,timedelta
from django.utils import timezone
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = 'mychat'
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message_to_db(self, message_text):
        message = Message(text=message_text, sender=self.user)
        message.save()
        return message

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        #waiting for sending delayed message
        if 'sendDateTime' in text_data_json:
            sendDateTime = datetime.fromtimestamp(text_data_json['sendDateTime']/1000.0).replace(tzinfo=None)
            now = timezone.localtime().replace(tzinfo=None)

            total =  (sendDateTime-now).total_seconds()
            await asyncio.sleep(total)


        message = await self.save_message_to_db(text_data_json['message'])
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': message.text,
                'sender': message.sender.username,
                'timestamp':message.timestamp.strftime("%d %b | %H:%M")
            }
        )

    # Called when someone wrote a messege to the chat
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'text': event['text'],
            'sender': event['sender'],
            'timestamp':event['timestamp']
        }))
