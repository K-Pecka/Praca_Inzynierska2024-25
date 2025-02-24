from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from trips.models import Trip
from .models import Itinerary, ItineraryActivity


class BaseItinerarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    trip = serializers.PrimaryKeyRelatedField(
        queryset=Trip.objects.all(),
    )

    class Meta:
        model = Itinerary
        fields = ['id', 'name', 'country', 'start_date', 'end_date', 'trip']


class ItinerarySerializer(BaseItinerarySerializer):

    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError(
                "Data zakończenia wycieczki nie może być wcześniejsza niż data rozpoczęcia.")
        return data

    class Meta(BaseItinerarySerializer.Meta):
        read_only_fields = ['id', 'name', 'country', 'start_date', 'end_date', 'trip']


class ItineraryCreateSerializer(BaseItinerarySerializer):
    class Meta(BaseItinerarySerializer.Meta):
        read_only_fields = ['id']


class ItineraryUpdateSerializer(BaseItinerarySerializer):
    class Meta(BaseItinerarySerializer.Meta):
        read_only_fields = ['id', 'trip']


class ItineraryDeleteSerializer(BaseItinerarySerializer):
    class Meta(BaseItinerarySerializer.Meta):
        read_only_fields = ['id']


class BaseItineraryActivitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=5120)
    location = serializers.CharField(max_length=100)
    start_time = serializers.TimeField()
    duration = serializers.IntegerField()
    itinerary = serializers.PrimaryKeyRelatedField(queryset=Itinerary.objects.all())

    class Meta:
        model = ItineraryActivity
        fields = ['id', 'name', 'type', 'description', 'location', 'start_time', 'duration', 'itinerary']


class ItineraryActivitySerializer(BaseItineraryActivitySerializer):

    class Meta(BaseItineraryActivitySerializer.Meta):
        read_only_fields = ['id', 'name', 'type', 'description', 'location', 'start_time', 'duration', 'itinerary']


class ItineraryActivityCreateSerializer(BaseItineraryActivitySerializer):
    class Meta(BaseItineraryActivitySerializer.Meta):
        read_only_fields = ['id']


class ItineraryActivityUpdateSerializer(BaseItineraryActivitySerializer):
    class Meta(BaseItineraryActivitySerializer.Meta):
        read_only_fields = ['id', 'itinerary']


class ItineraryActivityDeleteSerializer(BaseItineraryActivitySerializer):
    class Meta(BaseItineraryActivitySerializer.Meta):
        read_only_fields = ['id']
