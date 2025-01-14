from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from .models import Itinerary


class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = ['id', 'name', 'country', 'start_date', 'end_date', 'trip']

    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError(
                "Data zakończenia wycieczki nie może być wcześniejsza niż data rozpoczęcia.")
        return data
