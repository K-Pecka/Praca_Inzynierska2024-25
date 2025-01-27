from rest_framework import serializers
from .models import Trip, TripActivity, Ticket, Budget, Expense
from users.models import UserProfile


#################################################################
# Trip
#################################################################
class BaseTripSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    creator = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    members = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects.all())
    budget = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    settings = serializers.JSONField(required=False)

    class Meta:
        model = Trip
        fields = [
            'id', 'name', 'creator', 'members', 'budget', 'start_date', 'end_date', 'settings'
        ]


class TripSerializer(BaseTripSerializer):
    def validate(self, data):
        members = data.get("members", [])

        if members and data.get("creator") in members:
            raise serializers.ValidationError("Właściciel nie może być uczestnikiem wycieczki.")
        return data

    class Meta(BaseTripSerializer.Meta):
        read_only_fields = ['id', 'name', 'creator', 'members', 'budget', 'start_date', 'end_date', 'settings']


class TripCreateSerializer(BaseTripSerializer):
    def validate(self, data):
        request = self.context['request']
        members = data.get("members", [])

        if not request.user.is_guide:
            if Trip.objects.filter(creator=request.user.get_default_profile()).count() > 2:
                raise serializers.ValidationError("Osiągnąłeś limit wycieczek dla swojego profilu.")
        if members and data.get("creator") in members:
            raise serializers.ValidationError("Właściciel nie może być uczestnikiem wycieczki.")
        return data

    class Meta(BaseTripSerializer.Meta):
        read_only_fields = ['id', 'creator']


#################################################################
# TripActivity
#################################################################
class BaseTripActivitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    budget = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)
    description = serializers.CharField(max_length=500)
    date = serializers.DateTimeField()
    trip = serializers.PrimaryKeyRelatedField(required=False, queryset=Trip.objects.all())

    class Meta:
        model = TripActivity
        fields = [
            'id', 'name', 'budget', 'description', 'date', 'trip'
        ]


class TripActivitySerializer(BaseTripActivitySerializer):
    class Meta(BaseTripActivitySerializer.Meta):
        read_only_fields = ['id', 'name', 'budget', 'description', 'date', 'trip']


#################################################################
# Ticket
#################################################################
class BaseTicketSerializer(serializers.ModelSerializer):
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())
    profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    activity = serializers.PrimaryKeyRelatedField(queryset=TripActivity.objects.all())

    class Meta:
        model = Ticket
        fields = ['id', 'ticket', 'profile', 'trip', 'activity']


class TicketSerializer(BaseTicketSerializer):
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())
    profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    activity = serializers.PrimaryKeyRelatedField(queryset=TripActivity.objects.all())

    class Meta(BaseTicketSerializer.Meta):
        read_only_fields = ['id', 'profile', 'trip', 'activity']


class BudgetSerializer(serializers.ModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(required=True, queryset=Trip.objects.all())

    class Meta:
        model = Budget
        fields = [
            'id', 'amount', 'currency', 'trip'
        ]
        read_only_fields = ['id']


class ExpenseSerializer(serializers.ModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(required=True, queryset=Trip.objects.all())
    user = serializers.PrimaryKeyRelatedField(required=True, queryset=UserProfile.objects.all())

    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'date', 'description', 'trip', 'user', 'type'
        ]
        read_only_fields = ['id']
