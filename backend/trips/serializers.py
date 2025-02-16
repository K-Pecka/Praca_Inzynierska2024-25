from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import Trip, Ticket, Budget, Expense
from users.models import UserProfile


#################################################################
# Budget
#################################################################
# TODO: rozdzielić serializery
class BudgetSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=64)

    class Meta:
        model = Budget
        fields = [
            'id', 'amount', 'currency'
        ]
        read_only_fields = ['id',]

class BudgetCreateSerializer(BudgetSerializer):
    def create(self, validated_data):
        view = self.context['view']
        validated_data['trip'] = Trip.objects.get(pk=view.kwargs['trip_id'])
        return super().create(validated_data)

    class Meta(BudgetSerializer.Meta):
        read_only_fields = ['id',]



#################################################################
# Trip
#################################################################
class BaseTripSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    creator = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), required=False)
    members = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects.all())
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    settings = serializers.JSONField(required=False)

    class Meta:
        model = Trip
        fields = [
            'id', 'name', 'creator', 'members', 'start_date', 'end_date', 'settings'
        ]


class TripSerializer(BaseTripSerializer):
    budget = BudgetSerializer()

    def validate(self, data):
        members = data.get("members", [])

        if members and data.get("creator") in members:
            raise serializers.ValidationError("Właściciel nie może być uczestnikiem wycieczki.")
        return data

    def get_budget(self, obj):
        return obj.budget

    class Meta(BaseTripSerializer.Meta):
        fields = ['id', 'name', 'creator', 'members', 'budget', 'start_date', 'end_date', 'settings']


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

    def create(self, validated_data):
        try:
            request = self.context['request']
            validated_data['creator'] = request.user.get_default_profile()
            trip = super().create(validated_data)
            Budget.objects.create(currency='PLN', trip=trip)
            return trip
        except Exception as e:
            raise e

    class Meta(BaseTripSerializer.Meta):
        read_only_fields = ['id', 'creator']


#################################################################
# Ticket
#################################################################
class BaseTicketSerializer(serializers.ModelSerializer):
    ticket = serializers.FileField()
    profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    class Meta:
        model = Ticket
        fields = ['id', 'ticket', 'profile', 'trip']


class TicketSerializer(BaseTicketSerializer):
    class Meta(BaseTicketSerializer.Meta):
        read_only_fields = ['id', 'ticket', 'profile', 'trip']

#################################################################
# Expense
#################################################################
class ExpenseSerializer(serializers.ModelSerializer):
    budget = serializers.PrimaryKeyRelatedField(required=True, queryset=Budget.objects.all())
    user = serializers.PrimaryKeyRelatedField(required=True, queryset=UserProfile.objects.all())

    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'date', 'description', 'budget', 'user', 'type'
        ]
        read_only_fields = ['id']
