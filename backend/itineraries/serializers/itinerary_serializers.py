from rest_framework import serializers

from itineraries.models import Itinerary
from trips.models import Trip


class BaseItinerarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    trip = serializers.PrimaryKeyRelatedField(
        required=False,
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
    def create(self, validated_data):
        view = self.context['view']
        trip = Trip.objects.get(pk=view.kwargs.get('trip_pk'))
        validated_data['trip'] = trip
        return Itinerary.objects.create(**validated_data)

    class Meta(BaseItinerarySerializer.Meta):
        read_only_fields = ['id']


class ItineraryUpdateSerializer(BaseItinerarySerializer):
    class Meta(BaseItinerarySerializer.Meta):
        read_only_fields = ['id', 'trip']


class ItineraryDeleteSerializer(BaseItinerarySerializer):
    class Meta(BaseItinerarySerializer.Meta):
        read_only_fields = ['id']
