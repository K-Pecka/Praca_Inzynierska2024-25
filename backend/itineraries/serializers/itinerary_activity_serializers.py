from rest_framework import serializers

from itineraries.models import Itinerary, ItineraryActivity


class BaseItineraryActivitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=5120)
    location = serializers.CharField(max_length=100)
    start_time = serializers.TimeField()
    duration = serializers.IntegerField()
    itinerary = serializers.PrimaryKeyRelatedField(required=False, queryset=Itinerary.objects.all())

    class Meta:
        model = ItineraryActivity
        fields = ['id', 'name', 'type', 'description', 'location', 'start_time', 'duration', 'itinerary']


class ItineraryActivitySerializer(BaseItineraryActivitySerializer):
    class Meta(BaseItineraryActivitySerializer.Meta):
        read_only_fields = ['id', 'name', 'type', 'description', 'location', 'start_time', 'duration', 'itinerary']


class ItineraryActivityCreateSerializer(BaseItineraryActivitySerializer):
    def create(self, validated_data):
        view = self.context['view']
        itinerary_id = view.kwargs.get('itinerary_pk')
        validated_data['itinerary'] = Itinerary.objects.get(pk=itinerary_id)
        return ItineraryActivity.objects.create(**validated_data)

    class Meta(BaseItineraryActivitySerializer.Meta):
        read_only_fields = ['id']


class ItineraryActivityUpdateSerializer(BaseItineraryActivitySerializer):
    class Meta(BaseItineraryActivitySerializer.Meta):
        read_only_fields = ['id', 'itinerary']


class ItineraryActivityDeleteSerializer(BaseItineraryActivitySerializer):
    class Meta(BaseItineraryActivitySerializer.Meta):
        read_only_fields = ['id']
