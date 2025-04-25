import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from users.models import UserPrgit ofile
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_room"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]

        user_profile = await sync_to_async(UserProfile.objects.get)(user__username=username)

        await self.save_message(user_profile, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
        }))

    @sync_to_async
    def save_message(self, user_profile, message):
        Message.objects.create(profile=user_profile, content=message)

