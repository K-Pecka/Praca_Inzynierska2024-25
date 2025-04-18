from rest_framework import serializers

from itineraries.models import Itinerary, ItineraryActivity, ItineraryActivityType
from itineraries.serializers.itinerary_activity_type_serializers import ItineraryActivityTypeRetrieveSerializer, ItineraryActivityTypeListSerializer
from itineraries.serializers.itinerary_serializers import ItineraryRetrieveSerializer


class ItineraryActivityRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True, max_length=100)
    type = ItineraryActivityTypeRetrieveSerializer(read_only=True)
    description = serializers.CharField(read_only=True, max_length=5120)
    location = serializers.CharField(read_only=True, max_length=100)
    start_time = serializers.TimeField(read_only=True)
    duration = serializers.IntegerField(read_only=True)
    itinerary = ItineraryRetrieveSerializer(read_only=True)

    class Meta:
        model = ItineraryActivity
        fields = ['id', 'name', 'type', 'description', 'location', 'start_time', 'duration', 'itinerary']


class ItineraryActivityListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, max_length=100)
    type = ItineraryActivityTypeListSerializer(read_only=True)
    description = serializers.CharField(read_only=True, max_length=5120)
    location = serializers.CharField(read_only=True, max_length=100)
    start_time = serializers.TimeField(read_only=True)
    duration = serializers.IntegerField(read_only=True)
    itinerary = ItineraryRetrieveSerializer(read_only=True)

    class Meta:
        model = ItineraryActivity
        fields = ['name', 'type', 'description', 'location', 'start_time', 'duration', 'itinerary']


class ItineraryActivityCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    type = serializers.PrimaryKeyRelatedField(queryset=ItineraryActivityType.objects.all())
    description = serializers.CharField(max_length=5120)
    location = serializers.CharField(max_length=100)
    start_time = serializers.TimeField()
    duration = serializers.IntegerField()

    def create(self, validated_data):
        view = self.context['view']
        itinerary_id = view.kwargs.get('itinerary_pk')
        validated_data['itinerary'] = Itinerary.objects.get(pk=itinerary_id)
        return ItineraryActivity.objects.create(**validated_data)

    class Meta:
        model = ItineraryActivity
        fields = ["name", "type", "description", "location", "start_time", "duration", "itinerary"]


class ItineraryActivityUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, max_length=100)
    type = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ItineraryActivityType.objects.all())
    description = serializers.CharField(write_only=True, max_length=5120)
    location = serializers.CharField(write_only=True, max_length=100)
    start_time = serializers.TimeField(write_only=True)
    duration = serializers.IntegerField(write_only=True)

    class Meta:
        model = ItineraryActivity
        fields = ["name", "type", "description", "location", "start_time", "duration",]


class ItineraryActivityDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryActivity
        fields = ['id']
