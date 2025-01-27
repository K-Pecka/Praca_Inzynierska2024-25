from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from .models import Chatroom, ChatMessage
from trips.models import Trip
from users.models import UserProfile


class ChatroomSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    type = serializers.CharField(max_length=32)
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    creator = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    members = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects.all())
    settings = serializers.JSONField(max_length=1000)

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'type', 'trip', 'creator', 'members', 'settings']
        read_only_fields = ['id', 'name', 'type', 'trip', 'creator', 'members', 'settings']


class ChatroomCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    type = serializers.CharField(max_length=32)
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    creator = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    members = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects.all())
    settings = serializers.JSONField(max_length=1000)

    def validate(self, data):
        request = self.context['request']
        # TODO: walidacja dla prywatnych i publicznych pokoi dla przewodników i uczestników do ustalenia
        # if not request.user.is_guide:
        #     if Chatroom.objects.filter(creator=request.user.get_default_profile()).count() > 2:
        #         raise serializers.ValidationError("Osiągnąłeś limit wycieczek dla swojego profilu.")

    def validate_members(self, value):
        if len(value) != len(set(value)):
            # Check members duplicates
            raise serializers.ValidationError("Nie są dozwolone zduplikowane członkostwa.")
        return value

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'type', 'trip', 'creator', 'members', 'settings']
        read_only_fields = ['id']


class ChatroomUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    type = serializers.CharField(max_length=32)
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    creator = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    members = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects.all())
    settings = serializers.JSONField(max_length=1000)

    def validate_members(self, value):
        if len(value) != len(set(value)):
            # Check members duplicates
            raise serializers.ValidationError("Nie są dozwolone zduplikowane członkostwa.")
        return value

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'type', 'trip', 'creator', 'members', 'settings']
        read_only_fields = ['id', 'creator', 'trip']


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=512)
    profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    file = serializers.FileField(required=False)
    chatroom = serializers.PrimaryKeyRelatedField(queryset=Chatroom.objects.all())

    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'profile', 'file', 'chatroom']
        read_only_fields = ['id',]


class ChatMessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=512)
    profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    file = serializers.FileField(required=False)
    chatroom = serializers.PrimaryKeyRelatedField(queryset=Chatroom.objects.all())

    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'profile', 'file', 'chatroom']
        read_only_fields = ['id', 'text', 'profile', 'file', 'chatroom']


class ChatMessageUpdateSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=512)
    profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    file = serializers.FileField(required=False)
    chatroom = serializers.PrimaryKeyRelatedField(queryset=Chatroom.objects.all())

    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'profile', 'file', 'chatroom']
        read_only_fields = ['id', 'chatroom', 'profile']
