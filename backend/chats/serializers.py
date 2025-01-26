from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from .models import Chatroom, ChatMessage
from users.models import CustomUser

from trips.models import Trip

class ChatroomSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    type = serializers.CharField()
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    guide = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    tourists = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all())
    settings = serializers.CharField()

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'type', 'trip', 'guide', 'tourists', 'settings']
        read_only_fields = ['id']


class ChatroomCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    type = serializers.CharField()
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    guide = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    tourists = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all())
    settings = serializers.CharField()

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'type', 'trip', 'guide', 'tourists', 'settings']
        read_only_fields = ['id']


class ChatroomUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'type', 'trip', 'guide', 'tourists', 'settings']
        read_only_fields = ['id']


class ChatMessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    profile = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    file = serializers.FileField(required=False)
    chatroom = serializers.PrimaryKeyRelatedField(queryset=Chatroom.objects.all())

    class Meta:
        model = Chatroom
        fields = ['id', 'text', 'profile', 'file', 'chatroom']
        read_only_fields = ['id']


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = ['id', 'password']
        read_only_fields = ['id']
