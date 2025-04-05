from rest_framework import serializers

from trips.models import Ticket, TicketType, Trip
from users.models import UserProfile


class TicketCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    file = serializers.FileField()
    type = serializers.PrimaryKeyRelatedField(queryset=TicketType.objects.all())
    type_display = serializers.CharField(source='type.name', read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    valid_from = serializers.DateTimeField(
        format="%d.%m.%Y %H:%M",
        input_formats=["%d.%m.%Y %H:%M", "iso-8601"],
        help_text="Data w formacie DD.MM.RRRR GG:MM (np. 20.07.2023 14:30)",
        error_messages = {
            'invalid': 'Nieprawidłowy format daty. Wprowadź datę w formacie DD.MM.RRRR GG:MM',
            'blank': 'Data nie może być pusta',
            'null': 'Data nie może być pusta'
        }
    )
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    def create(self, validated_data):
        view = self.context['view']
        profile = view.request.user.get_default_profile()
        validated_data['profile'] = profile
        return Ticket.objects.create(**validated_data)

    class Meta:
        model = Ticket
        fields = ['id', 'file', 'type', 'type_display', 'profile', 'valid_from', 'trip']


class TicketRetrieveSerializer(serializers.ModelSerializer):
    file = serializers.FileField(read_only=True)
    type = serializers.PrimaryKeyRelatedField(read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    valid_from = serializers.DateTimeField(
        read_only=True,
        format="%d.%m.%Y %H:%M",
    )
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Ticket
        fields = ['file', 'type', 'profile', 'valid_from', 'trip']

class TicketListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    file = serializers.FileField(read_only=True)
    type = serializers.PrimaryKeyRelatedField(read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    valid_from = serializers.DateTimeField(
        format="%d.%m.%Y %H:%M",
    )
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Ticket
        fields = ['id', 'file', 'type', 'profile', 'valid_from', 'trip']

class TicketUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    file = serializers.FileField()
    type = serializers.PrimaryKeyRelatedField(queryset=TicketType.objects.all())
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    valid_from = serializers.DateTimeField(
        format="%d.%m.%Y %H:%M",
        input_formats=["%d.%m.%Y %H:%M", "iso-8601"],
    )
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Ticket
        fields = ['id', 'file', 'type', 'profile', 'valid_from', 'trip']

class TicketDestroySerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ['id']