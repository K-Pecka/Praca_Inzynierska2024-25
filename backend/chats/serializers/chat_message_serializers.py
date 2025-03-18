from rest_framework import serializers

from chats.models import ChatMessage, Chatroom


class BaseChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'profile', 'file', 'chatroom']


class ChatMessageCreateSerializer(BaseChatMessageSerializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=512)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    file = serializers.FileField(required=False)
    chatroom = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        view = self.context.get('view')
        profile = view.request.user.get_default_profile()
        validated_data['profile'] = profile

        chatroom_id = view.kwargs.get('room_pk')
        if not chatroom_id:
            raise serializers.ValidationError("ID pokoju jest wymagane.")

        try:
            chatroom = Chatroom.objects.get(pk=chatroom_id)
        except Chatroom.DoesNotExist:
            raise serializers.ValidationError("Pokój o podanym id nie istnieje.")

        validated_data['chatroom'] = chatroom
        return ChatMessage.objects.create(**validated_data)


class ChatMessageRetrieveSerializer(BaseChatMessageSerializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(read_only=True, max_length=512)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    file = serializers.FileField(read_only=True)
    chatroom = serializers.PrimaryKeyRelatedField(read_only=True)


class ChatMessageListSerializer(BaseChatMessageSerializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(read_only=True, max_length=512)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    file = serializers.FileField(read_only=True)
    chatroom = serializers.PrimaryKeyRelatedField(read_only=True)


class ChatMessageUpdateSerializer(BaseChatMessageSerializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=512)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    file = serializers.FileField(required=False)
    chatroom = serializers.PrimaryKeyRelatedField(read_only=True)
