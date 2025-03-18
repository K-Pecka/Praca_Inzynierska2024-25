from rest_framework import serializers

from chats.models import Chatroom
from users.models import UserProfile


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
