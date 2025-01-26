from rest_framework import serializers
from .models import Trip, TripActivity, Ticket
from users.models import UserProfile


# Trip Serializer
class TripSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(required=True, queryset=UserProfile.objects.all())
    members = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects.all())

    class Meta:
        model = Trip
        fields = [
            'id', 'name', 'creator', 'members', 'budget', 'start_date', 'end_date', 'settings'
        ]
        read_only_fields = ['id', 'creator']


class TripCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    creator = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    members = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects.all())
    budget = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    settings = serializers.JSONField(required=False)

    def validate(self, data):
        request = self.context['request']
        if not request.user.is_guide:
            if Trip.objects.filter(creator=request.user.get_default_profile()).count() > 2:
                raise serializers.ValidationError("Osiągnąłeś limit wycieczek dla swojego profilu.")
        return data

    class Meta:
        model = Trip
        fields = [
            'id', 'name', 'creator', 'members', 'budget', 'start_date', 'end_date', 'settings'
        ]
        read_only_fields = ['id', 'creator']


# TripActivity Serializer
class TripActivitySerializer(serializers.ModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(required=False, queryset=Trip.objects.all())

    class Meta:
        model = TripActivity
        fields = [
            'id', 'name', 'budget', 'description', 'date', 'trip'
        ]
        read_only_fields = ['id', 'date']


# Ticket Serializer
class TicketSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(required=True, queryset=UserProfile.objects.all())
    trip = serializers.PrimaryKeyRelatedField(required=True, queryset=Trip.objects.all())
    activity = serializers.PrimaryKeyRelatedField(required=True, queryset=TripActivity.objects.all())

    class Meta:
        model = Ticket
        fields = [
            'id', 'ticket', 'profile', 'trip', 'activity'
        ]
        read_only_fields = ['id', 'profile']
