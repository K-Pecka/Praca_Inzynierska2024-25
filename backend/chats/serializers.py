from rest_framework import serializers

from .models import Chatroom, ChatMessage
from users.models import UserProfile


#####################################################################
# Chatroom
#####################################################################
class BaseChatroomSerializer(serializers.ModelSerializer):
    def validate_members(self, value):
        # Ensure no duplicate members
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Użytkownicy nie mogą się powtarzać.")
        return value

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'type', 'trip', 'creator', 'members', 'settings']


class ChatroomCreateSerializer(BaseChatroomSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=30)
    type = serializers.CharField(max_length=32)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects.all())
    settings = serializers.JSONField()

    def validate(self, data):
        # TODO: walidacja dla prywatnych i publicznych pokoi dla przewodników i uczestników do ustalenia
        return data


class ChatroomRetrieveSerializer(BaseChatroomSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True, max_length=30)
    type = serializers.CharField(read_only=True, max_length=32)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(read_only=True)
    settings = serializers.JSONField(read_only=True)


class ChatroomListSerializer(BaseChatroomSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True, max_length=30)
    type = serializers.CharField(read_only=True, max_length=32)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(read_only=True)
    settings = serializers.JSONField(read_only=True)


class ChatroomUpdateSerializer(BaseChatroomSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=30)
    type = serializers.CharField(max_length=32)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all())
    settings = serializers.JSONField()


#####################################################################
# ChatMessage
#####################################################################
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
