from rest_framework import serializers

from trips.models import Ticket, TicketType, Trip
from users.models import UserProfile


class BaseTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'file', 'type', 'profile', 'valid_from', 'trip']


class TicketCreateSerializer(BaseTicketSerializer):
    id = serializers.IntegerField(read_only=True)
    file = serializers.FileField()
    type = serializers.PrimaryKeyRelatedField(queryset=TicketType.objects.all())
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    valid_from = serializers.DateTimeField()
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    def create(self, validated_data):
        view = self.context['view']
        profile = view.request.user.get_default_profile()
        validated_data['profile'] = profile
        return Ticket.objects.create(**validated_data)


class TicketRetrieveSerializer(BaseTicketSerializer):
    id = serializers.IntegerField(read_only=True)
    file = serializers.FileField(read_only=True)
    type = serializers.PrimaryKeyRelatedField(read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    valid_from = serializers.DateTimeField(read_only=True)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)


class TicketListSerializer(BaseTicketSerializer):
    id = serializers.IntegerField(read_only=True)
    file = serializers.FileField(read_only=True)
    type = serializers.PrimaryKeyRelatedField(read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    valid_from = serializers.DateTimeField(read_only=True)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)


class TicketUpdateSerializer(BaseTicketSerializer):
    id = serializers.IntegerField(read_only=True)
    file = serializers.FileField()
    type = serializers.PrimaryKeyRelatedField(queryset=TicketType.objects.all())
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    valid_from = serializers.DateTimeField()
    trip = serializers.PrimaryKeyRelatedField(read_only=True)



class TicketDestroySerializer(BaseTicketSerializer):
    id = serializers.IntegerField(write_only=True)
    file = serializers.FileField(write_only=True)
    type = serializers.PrimaryKeyRelatedField(write_only=True, queryset=TicketType.objects.all())
    profile = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserProfile.objects.all())
    valid_from = serializers.DateTimeField(write_only=True)
    trip = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Trip.objects.all())
