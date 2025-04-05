from rest_framework import serializers

from chats.choices import ChatroomType
from chats.models import Chatroom
from trips.models import Trip
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

    def create(self, validated_data):
        try:
            request = self.context['request']
            kwargs = self.context['view'].kwargs
            trip_id = kwargs.pop('trip_pk', None)
            trip = Trip.objects.get(id=trip_id)
            if not trip:
                raise serializers.ValidationError("Nie znaleziono wycieczki.")

            validated_data['creator'] = request.user.get_default_profile()
            validated_data['trip'] = trip
            chatroom = super().create(validated_data)
            return chatroom
        except Exception as e:
            raise e


class ChatroomRetrieveSerializer(BaseChatroomSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True, max_length=30)
    type = serializers.CharField(read_only=True, max_length=32)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    settings = serializers.JSONField(read_only=True)


class ChatroomListSerializer(BaseChatroomSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True, max_length=30)
    type = serializers.CharField(read_only=True, max_length=32)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    settings = serializers.JSONField(read_only=True)


class ChatroomUpdateSerializer(BaseChatroomSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=30)
    type = serializers.CharField(max_length=32)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all())
    settings = serializers.JSONField()
