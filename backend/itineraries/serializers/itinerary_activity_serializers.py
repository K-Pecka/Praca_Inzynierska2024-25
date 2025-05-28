from rest_framework import serializers

from itineraries.models import Itinerary, ItineraryActivity, ItineraryActivityType
from trips.models import Ticket


class ItineraryActivityRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True, max_length=100)
    ticket = serializers.PrimaryKeyRelatedField(read_only=True)
    type = serializers.PrimaryKeyRelatedField(read_only=True)
    description = serializers.CharField(read_only=True, max_length=5120)
    location = serializers.CharField(read_only=True, max_length=100)
    date = serializers.DateField(read_only=True)
    start_time = serializers.TimeField(read_only=True)
    duration = serializers.IntegerField(read_only=True)
    itinerary = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ItineraryActivity
        fields = ['id', 'name', 'ticket', 'type', 'description', 'location', 'date', 'start_time', 'duration', 'itinerary']


class ItineraryActivityListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True, max_length=100)
    type = serializers.PrimaryKeyRelatedField(read_only=True)
    ticket = serializers.PrimaryKeyRelatedField(read_only=True)
    description = serializers.CharField(read_only=True, max_length=5120)
    location = serializers.CharField(read_only=True, max_length=100)
    date = serializers.DateField(read_only=True)
    start_time = serializers.TimeField(read_only=True)
    duration = serializers.IntegerField(read_only=True)
    itinerary = serializers.PrimaryKeyRelatedField(read_only=True)
    itinerary_for_today = serializers.IntegerField(read_only=True)
    itinerary_for_week = serializers.IntegerField(read_only=True)

    class Meta:
        model = ItineraryActivity
        fields = ['id', 'name', 'type', 'ticket', 'description', 'location', 'date', 'start_time', 'duration', 'itinerary', 'itinerary_for_today', 'itinerary_for_week']


class ItineraryActivityCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), required=False)
    type = serializers.PrimaryKeyRelatedField(queryset=ItineraryActivityType.objects.all())
    description = serializers.CharField(max_length=5120, required=False)
    location = serializers.CharField(max_length=100, required=False)
    date = serializers.DateField()
    start_time = serializers.TimeField(required=False)
    duration = serializers.IntegerField(required=False)

    def create(self, validated_data):
        view = self.context['view']
        itinerary_id = view.kwargs.get('itinerary_pk')
        validated_data['itinerary'] = Itinerary.objects.get(pk=itinerary_id)
        return ItineraryActivity.objects.create(**validated_data)

    class Meta:
        model = ItineraryActivity
        fields = ["name", "ticket", "type", "description", "location", "date", "start_time", "duration"]


class ItineraryActivityUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, max_length=100, required=False)
    type = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ItineraryActivityType.objects.all(), required=False)
    ticket = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Ticket.objects.all(), required=False)
    description = serializers.CharField(write_only=True, max_length=5120, required=False)
    location = serializers.CharField(write_only=True, max_length=100, required=False)
    date = serializers.DateField(write_only=True, required=False)
    start_time = serializers.TimeField(write_only=True, required=False)
    duration = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = ItineraryActivity
        fields = ["name", "type", "ticket", "description", "location", "date", "start_time", "duration"]


class ItineraryActivityDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryActivity
        fields = ['id']
