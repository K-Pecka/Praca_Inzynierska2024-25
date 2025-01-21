from rest_framework import serializers
from .models import Trip, TripActivity, Ticket
from ..users.models import UserProfile


# Trip Serializer
class TripSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(required=True, read_only=True)
    members = serializers.PrimaryKeyRelatedField(required=True, queryset=UserProfile.objects.all())

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
    profile = serializers.StringRelatedField(required=True, read_only=True)
    trip = serializers.PrimaryKeyRelatedField(required=True, queryset=Trip.objects.all())
    activity = serializers.PrimaryKeyRelatedField(required=True, queryset=TripActivity.objects.all())

    class Meta:
        model = Ticket
        fields = [
            'id', 'ticket', 'profile', 'trip', 'activity'
        ]
        read_only_fields = ['id', 'profile']
