import json
import traceback

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Chatroom
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_name}"

        user = self.scope.get("user")
        if not user or user.is_anonymous:
            print("❌ Użytkownik nieautoryzowany – rozłączam.")
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"✅ WebSocket połączony z room_id={self.room_name}, user_id={user.id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"🔌 WebSocket rozłączony (code {close_code})")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("content")
            user = self.scope["user"]

            if user.is_anonymous:
                print("❌ Odebrano wiadomość od anonimowego użytkownika.")
                await self.close()
                return

            if not message:
                print("⚠️ Odebrano pustą wiadomość – pomijam.")
                return

            msg = await self.save_message(user.profile, int(self.room_name), message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "id": msg.id,
                    "message": msg.content,
                    "sender_id": msg.profile.id,
                    "created": msg.created.isoformat(),
                }
            )
            print(f"📤 Wiadomość zapisana i wysłana: {msg.content}")

        except Exception as e:
            print("❌ Błąd w receive():", str(e))
            traceback.print_exc()
            await self.close()

    async def chat_message(self, event):
        try:
            await self.send(text_data=json.dumps({
                "id": event["id"],
                "content": event["message"],
                "sender_id": event["sender_id"],
                "created": event["created"],
            }))
        except Exception as e:
            print("❌ Błąd w chat_message():", str(e))
            traceback.print_exc()

    @sync_to_async
    def save_message(self, profile, room_id, content):
        room = Chatroom.objects.get(id=room_id)
        return Message.objects.create(
            profile=profile,
            chatroom=room,
            content=content
        )
