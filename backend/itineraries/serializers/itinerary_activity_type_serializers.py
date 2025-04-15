from rest_framework import serializers

from itineraries.models import ItineraryActivityType


class ItineraryActivityTypeRetrieveSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, max_length=100)

    class Meta:
        model = ItineraryActivityType
        fields = ['name']


class ItineraryActivityTypeListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True, max_length=100)

    class Meta:
        model = ItineraryActivityType
        fields = ['id', 'name']