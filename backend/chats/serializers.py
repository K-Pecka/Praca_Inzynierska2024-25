from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from .models import Chatroom, ChatMessage
from trips.models import Trip
from users.models import UserProfile


#####################################################################
# Chatroom
#####################################################################
class BaseChatroomSerializer(serializers.ModelSerializer):
    def validate_members(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Nie są dozwolone zduplikowane członkostwa.")
        return value

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'type', 'trip', 'creator', 'members', 'settings']


class ChatroomCreateSerializer(BaseChatroomSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=30)
    type = serializers.CharField(max_length=32)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all())
    settings = serializers.JSONField()

    def validate(self, data):
        # TODO: walidacja dla prywatnych i publicznych pokoi dla przewodników i uczestników do ustalenia
        return data


class ChatroomRetrieveSerializer(BaseChatroomSerializer):
    id = serializers.IntegerField(write_only=True)
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
    id = serializers.IntegerField(write_only=True)
    name = serializers.CharField(max_length=30)
    type = serializers.CharField(max_length=32)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all())
    settings = serializers.JSONField()


class ChatroomDestroySerializer(BaseChatroomSerializer):
    id = serializers.IntegerField(write_only=True)
    name = serializers.CharField(write_only=True, max_length=30)
    type = serializers.CharField(write_only=True, max_length=32)
    trip = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Trip.objects.all())
    creator = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserProfile.objects.all())
    members = serializers.PrimaryKeyRelatedField(write_only=True, many=True, queryset=UserProfile.objects.all())
    settings = serializers.JSONField(write_only=True)


#####################################################################
# ChatMessage
#####################################################################
class BaseChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'profile', 'file', 'chatroom']


class ChatMessageCreateSerializer(BaseChatMessageSerializer):
    id = serializers.IntegerField(write_only=True)
    text = serializers.CharField(max_length=512)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    file = serializers.FileField()
    chatroom = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        view = self.context.get('view')
        profile = view.request.user.get_default_profile()
        validated_data['profile'] = profile
        chatroom_id = view.kwargs.get('room_id')
        chatroom = Chatroom.objects.get(pk=chatroom_id)
        validated_data['chatroom'] = chatroom
        return Chatroom.objects.create(**validated_data)


class ChatMessageRetrieveSerializer(BaseChatMessageSerializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(write_only=True, max_length=512)
    profile = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserProfile.objects.all())
    file = serializers.FileField(write_only=True)
    chatroom = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Chatroom.objects.all())


class ChatMessageListSerializer(BaseChatMessageSerializer):
    id = serializers.IntegerField(write_only=True)
    text = serializers.CharField(write_only=True, max_length=512)
    profile = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserProfile.objects.all())
    file = serializers.FileField(write_only=True)
    chatroom = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Chatroom.objects.all())


class ChatMessageUpdateSerializer(BaseChatMessageSerializer):
    id = serializers.IntegerField(write_only=True)
    text = serializers.CharField(max_length=512)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    file = serializers.FileField()
    chatroom = serializers.PrimaryKeyRelatedField(read_only=True)


class ChatMessageDestroySerializer(BaseChatMessageSerializer):
    id = serializers.IntegerField(write_only=True)
    text = serializers.CharField(write_only=True, max_length=512)
    profile = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserProfile.objects.all())
    file = serializers.FileField(write_only=True)
    chatroom = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Chatroom.objects.all())
