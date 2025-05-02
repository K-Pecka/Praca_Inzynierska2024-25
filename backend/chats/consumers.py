import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chats.models import Message
from users.models import UserProfile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_name}"

        user = self.scope.get("user")
        if user is None or user.is_anonymous:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(f"✅ WebSocket połączony z room_id={self.room_name}, user_id={user.id}")
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"🔌 WebSocket rozłączony (code {close_code})")

    async def receive(self, text_data):
        user = self.scope["user"]
        try:
            data = json.loads(text_data)
            message = data.get("content", "")

            if not message:
                return

            profile = await database_sync_to_async(user.get_default_profile)()
            msg = await self.save_message(profile, int(self.room_name), message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "id": msg.id,
                    "message": msg.content,
                    "sender_id": profile.id,
                    "created": msg.created.isoformat(),
                }
            )
        except Exception as e:
            print("❌ Błąd w receive():", e)
            await self.close()

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, profile, room_id, content):
        return Message.objects.create(
            profile=profile,
            chatroom_id=room_id,
            content=content
        )
