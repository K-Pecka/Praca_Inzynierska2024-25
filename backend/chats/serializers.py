from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from .models import Chatroom, ChatMessage
from trips.models import Trip
from users.models import UserProfile


#####################################################################
# Chatroom
#####################################################################
class BaseChatroomSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    type = serializers.CharField(max_length=32)
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    creator = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    members = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects.all())
    settings = serializers.JSONField()

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'type', 'trip', 'creator', 'members', 'settings']


class ChatroomSerializer(BaseChatroomSerializer):
    class Meta(BaseChatroomSerializer.Meta):
        read_only_fields = ['id', 'name', 'type', 'trip', 'creator', 'members', 'settings']


class ChatroomCreateSerializer(BaseChatroomSerializer):
    def validate(self, data):
        request = self.context['request']
        # TODO: walidacja dla prywatnych i publicznych pokoi dla przewodników i uczestników do ustalenia
        return data
        # if not request.user.is_guide:
        #     if Chatroom.objects.filter(creator=request.user.get_default_profile()).count() > 2:
        #         raise serializers.ValidationError("Osiągnąłeś limit wycieczek dla swojego profilu.")

    def validate_members(self, value):
        if len(value) != len(set(value)):
            # Check members duplicates
            raise serializers.ValidationError("Nie są dozwolone zduplikowane członkostwa.")
        return value

    class Meta(BaseChatroomSerializer.Meta):
        model = Chatroom
        read_only_fields = ['id']


class ChatroomUpdateSerializer(BaseChatroomSerializer):
    def validate_members(self, value):
        if len(value) != len(set(value)):
            # Check members duplicates
            raise serializers.ValidationError("Nie są dozwolone zduplikowane członkostwa.")
        return value

    class Meta(BaseChatroomSerializer.Meta):
        model = Chatroom
        read_only_fields = ['id', 'creator', 'trip']


#####################################################################
# ChatMessage
#####################################################################
class BaseChatMessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=512)
    profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    file = serializers.FileField(required=False)
    chatroom = serializers.PrimaryKeyRelatedField(queryset=Chatroom.objects.all())

    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'profile', 'file', 'chatroom']


class ChatMessageCreateSerializer(BaseChatMessageSerializer):
    class Meta(BaseChatMessageSerializer.Meta):
        model = ChatMessage
        read_only_fields = ['id', ]


class ChatMessageSerializer(BaseChatMessageSerializer):
    class Meta(BaseChatMessageSerializer.Meta):
        model = ChatMessage
        read_only_fields = ['id', 'text', 'profile', 'file', 'chatroom']


class ChatMessageUpdateSerializer(BaseChatMessageSerializer):
    class Meta(BaseChatMessageSerializer.Meta):
        model = ChatMessage
        read_only_fields = ['id', 'chatroom', 'profile']
