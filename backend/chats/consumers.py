import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Chatroom
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_name}"

        # user = self.scope.get("user")
        # if user is None or user.is_anonymous:
        #     await self.close()
        #     return

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
        message = data["content"]
        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
            return

        # Zapisz wiadomość
        await self.save_message(user.profile, int(self.room_name), message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": user.profile.id,
                "created": self.get_now(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "content": event["message"],
            "sender_id": event["sender_id"],
            "created": event["created"],
        }))

    @sync_to_async
    def save_message(self, profile, room_id, content):
        room = Chatroom.objects.get(id=room_id)
        return Message.objects.create(
            profile=profile,
            chatroom=room,
            content=content
        )

    def get_now(self):
        from django.utils.timezone import now
        return now().isoformat()
