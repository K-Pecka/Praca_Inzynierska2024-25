from rest_framework import serializers

from .models import Chatroom, ChatMessage

from trips.models import Trip

from users.models import UserProfile


class ChatroomSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    type = serializers.CharField()
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    creator = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all(), required=False)
    settings = serializers.JSONField()

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'type', 'trip', 'creator', 'members', 'settings']
        read_only_fields = ['id']


class ChatroomCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    type = serializers.CharField()
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    creator = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all(), required=False)
    settings = serializers.JSONField()

    def validate_members(self, value):
        # Custom validation method
        if len(value) != len(set(value)):
            # Check members duplicates
            raise serializers.ValidationError("Duplicate members are not allowed.")
        if self.creator in value:
            # Check if creator is also a tourist
            raise serializers.ValidationError("Creator cannot be a tourist.")
        return value

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'type', 'trip', 'creator', 'members', 'settings']
        read_only_fields = ['id']


class ChatroomUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    type = serializers.CharField()
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    creator = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all(), required=False)
    settings = serializers.JSONField()

    def validate_members(self, value):
        # Check members duplicates
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate members are not allowed.")
        return value

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'type', 'trip', 'creator', 'members', 'settings']
        read_only_fields = ['id']


class ChatMessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    file = serializers.FileField(required=False)
    chatroom = serializers.PrimaryKeyRelatedField(queryset=Chatroom.objects.all())

    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'profile', 'file', 'chatroom']
        read_only_fields = ['id']


class ChatMessageUpdateSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    file = serializers.FileField(required=False)
    chatroom = serializers.PrimaryKeyRelatedField(queryset=Chatroom.objects.all())

    def validate(self, data):
        if self.instance and self.instance.profile != data['profile']:
            raise serializers.ValidationError("Changing the profile of a message is not allowed.")
        if self.instance and self.instance.chatroom != data['chatroom']:
            raise serializers.ValidationError("Changing the chatroom of a message is not allowed.")
        return data

    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'profile', 'file', 'chatroom']
        read_only_fields = ['id']


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    file = serializers.FileField(required=False)
    chatroom = serializers.PrimaryKeyRelatedField(queryset=Chatroom.objects.all())

    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'profile', 'file', 'chatroom']
        read_only_fields = ['id']



