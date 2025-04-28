from rest_framework import serializers

from trips.models import Ticket, TicketType, Trip
from users.models import UserProfile


class TicketCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    file = serializers.FileField()
    type = serializers.PrimaryKeyRelatedField(queryset=TicketType.objects.all())
    type_display = serializers.CharField(source='type.name', read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    valid_from_date = serializers.DateField(
        format="%d.%m.%Y",
        input_formats=["%d.%m.%Y", "iso-8601"],
        help_text="Data w formacie DD.MM.RRRR (np. 20.07.2023)",
        error_messages = {
            'invalid': 'Nieprawidłowy format daty. Wprowadź datę w formacie DD.MM.RRRR',
            'blank': 'Data nie może być pusta',
            'null': 'Data nie może być pusta'
        }
    )
    valid_from_time = serializers.TimeField(
        format="%H:%M",
        input_formats=["%H:%M", "iso-8601"],
        help_text="Czas w formacie GG:MM (np. 14:30)",
        error_messages = {
            'invalid': 'Nieprawidłowy format czasu. Wprowadź czas w formacie GG:MM',
            'blank': 'Czas nie może być pusty',
            'null': 'Czas nie może być pusty'
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
        fields = ['id', 'name', 'file', 'type', 'type_display', 'profile', 'valid_from_date', 'valid_from_time', 'trip']


class TicketRetrieveSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    file = serializers.FileField(read_only=True)
    type = serializers.PrimaryKeyRelatedField(read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    valid_from_date = serializers.DateField(
        read_only=True,
        format="%d.%m.%Y",
    )
    valid_from_time = serializers.TimeField(
        read_only=True,
        format="%H:%M",
    )
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Ticket
        fields = ['name', 'file', 'type', 'profile', 'valid_from_date', 'valid_from_time', 'trip']

class TicketListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    file = serializers.FileField(read_only=True)
    type = serializers.PrimaryKeyRelatedField(read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    valid_from_date = serializers.DateField(
        read_only=True,
        format="%d.%m.%Y",
    )
    valid_from_time = serializers.TimeField(
        read_only=True,
        format="%H:%M",
    )
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Ticket
        fields = ['id', 'name', 'file', 'type', 'profile', 'valid_from_date', 'valid_from_time', 'trip']

class TicketUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    file = serializers.FileField()
    type = serializers.PrimaryKeyRelatedField(queryset=TicketType.objects.all())
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    valid_from_date = serializers.DateField(
        format="%d.%m.%Y",
        input_formats=["%d.%m.%Y", "iso-8601"],
    )
    valid_from_time = serializers.TimeField(
        format="%H:%M",
        input_formats=["%H:%M", "iso-8601"],
    )
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Ticket
        fields = ['id', 'name', 'file', 'type', 'profile', 'valid_from_date', 'valid_from_time', 'trip']

class TicketDestroySerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ['id']