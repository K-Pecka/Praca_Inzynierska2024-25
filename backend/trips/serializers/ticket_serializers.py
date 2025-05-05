from rest_framework import serializers

from trips.models import Ticket, TicketType, Trip
from users.models import UserProfile


class TicketCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    file = serializers.FileField()
    type = serializers.PrimaryKeyRelatedField(queryset=TicketType.objects.all())
    type_display = serializers.CharField(source='type.name', read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    profiles = serializers.PrimaryKeyRelatedField(
        many=True, queryset=UserProfile.objects.all(), required=False
    )
    trip = serializers.PrimaryKeyRelatedField(
        queryset=Trip.objects.all(), write_only=True, required=False
    )
    valid_from_date = serializers.DateField(
        format="%d.%m.%Y",
        input_formats=["%d.%m.%Y", "iso-8601"],
        help_text="Data w formacie DD.MM.RRRR",
        error_messages={
            'invalid': 'Nieprawidłowy format daty.',
            'blank': 'Data nie może być pusta',
            'null': 'Data nie może być pusta'
        }
    )
    valid_from_time = serializers.TimeField(
        format="%H:%M",
        input_formats=["%H:%M", "iso-8601"],
        help_text="Czas w formacie GG:MM",
        error_messages={
            'invalid': 'Nieprawidłowy format czasu.',
            'blank': 'Czas nie może być pusty',
            'null': 'Czas nie może być pusty'
        }
    )

    def create(self, validated_data):
        view = self.context['view']
        owner = view.request.user.get_default_profile()
        profiles = validated_data.pop('profiles', [])

        if owner not in profiles:
            profiles.append(owner)

        ticket = Ticket.objects.create(owner=owner, **validated_data)
        ticket.profiles.set(profiles)
        return ticket

    class Meta:
        model = Ticket
        fields = [
            'id', 'name', 'file', 'type', 'type_display',
            'owner', 'profiles', 'valid_from_date', 'valid_from_time', 'trip'
        ]


class TicketRetrieveSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    file = serializers.FileField(read_only=True)
    type = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    profiles = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    valid_from_date = serializers.DateField(read_only=True, format="%d.%m.%Y")
    valid_from_time = serializers.TimeField(read_only=True, format="%H:%M")
    trip = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'name', 'file', 'type', 'owner', 'profiles',
            'valid_from_date', 'valid_from_time', 'trip'
        ]


class TicketListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    file = serializers.FileField(read_only=True)
    type = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    profiles = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    valid_from_date = serializers.DateField(read_only=True, format="%d.%m.%Y")
    valid_from_time = serializers.TimeField(read_only=True, format="%H:%M")
    trip = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'name', 'file', 'type', 'owner', 'profiles',
            'valid_from_date', 'valid_from_time', 'trip'
        ]


class TicketUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    file = serializers.FileField()
    type = serializers.PrimaryKeyRelatedField(queryset=TicketType.objects.all())
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    profiles = serializers.PrimaryKeyRelatedField(
        many=True, queryset=UserProfile.objects.all(), required=False
    )
    valid_from_date = serializers.DateField(
        format="%d.%m.%Y",
        input_formats=["%d.%m.%Y", "iso-8601"]
    )
    valid_from_time = serializers.TimeField(
        format="%H:%M",
        input_formats=["%H:%M", "iso-8601"]
    )
    trip = serializers.PrimaryKeyRelatedField(read_only=True)

    def update(self, instance, validated_data):
        profiles = validated_data.pop('profiles', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if profiles is not None:
            instance.profiles.set(profiles)
        return instance

    class Meta:
        model = Ticket
        fields = [
            'id', 'name', 'file', 'type', 'owner', 'profiles',
            'valid_from_date', 'valid_from_time', 'trip'
        ]


class TicketDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        read_only_fields = ['id']
        fields = ['id']
