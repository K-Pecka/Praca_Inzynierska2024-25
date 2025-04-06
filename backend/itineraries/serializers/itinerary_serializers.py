from rest_framework import serializers

from itineraries.models import Itinerary
from trips.models import Trip


class ItineraryRetrieveSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, read_only=True)
    country = serializers.CharField(max_length=100, read_only=True)
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    trip = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError(
                "Data zakończenia wycieczki nie może być wcześniejsza niż data rozpoczęcia.")
        return data

    class Meta:
        model = Itinerary
        fields = ['id', 'name', 'country', 'start_date', 'end_date', 'trip']


class ItineraryCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    trip = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    def create(self, validated_data):
        view = self.context['view']
        trip = Trip.objects.get(pk=view.kwargs.get('trip_pk'))
        validated_data['trip'] = trip
        return Itinerary.objects.create(**validated_data)

    class Meta:
        model = Itinerary
        fields = ['id', 'name', 'country', 'start_date', 'end_date', 'trip']
        read_only_fields = ['id', 'trip']


class ItineraryUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    trip = serializers.PrimaryKeyRelatedField(
        required=False,
        read_only=True
    )
    class Meta:
        model = Itinerary
        fields = ['id', 'name', 'country', 'start_date', 'end_date', 'trip']
        read_only_fields = ['id', 'trip']


class ItineraryDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = ['id']
