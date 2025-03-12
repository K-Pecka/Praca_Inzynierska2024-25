from rest_framework import serializers

from django.shortcuts import get_object_or_404
from users.serializers import UserListSerializer

from .models import Trip, Ticket, Budget, Expense
from users.models import UserProfile


#################################################################
# Budget
#################################################################
class BudgetBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'amount', 'currency', 'trip']


class BudgetRetrieveSerializer(BudgetBaseSerializer):
    id = serializers.IntegerField(read_only=True)
    amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    currency = serializers.CharField(read_only=True, max_length=64)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)


class BudgetUpdateSerializer(BudgetBaseSerializer):
    id = serializers.IntegerField(read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=64)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)


class BudgetDestroySerializer(BudgetBaseSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.DecimalField(write_only=True, max_digits=10, decimal_places=2)
    currency = serializers.CharField(write_only=True, max_length=64)
    trip = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Trip.objects.all())


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


class TripRetrieveSerializer(BaseTripSerializer):
    id = serializers.IntegerField(write_only=True)
    name = serializers.CharField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = UserListSerializer(read_only=True, many=True)
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    settings = serializers.JSONField(read_only=True)
    budget = BudgetRetrieveSerializer(read_only=True)

    def get_budget(self, obj):
        return obj.budget


class TripListSerializer(TripRetrieveSerializer):
    id = serializers.IntegerField(read_only=True)
    members = UserListSerializer(read_only=True, many=True)


class TripUpdateSerializer(BaseTripSerializer):
    id = serializers.IntegerField(write_only=True)
    name = serializers.CharField()
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all())
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    settings = serializers.JSONField()
    budget = BudgetRetrieveSerializer()
    # TODO: walidacja start_date end_date czy mozna zmienic


class TripDestroySerializer(BaseTripSerializer):
    id = serializers.IntegerField(write_only=True)
    name = serializers.CharField(write_only=True)
    creator = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserProfile.objects.all())
    members = serializers.PrimaryKeyRelatedField(write_only=True, many=True, queryset=UserProfile.objects.all())
    start_date = serializers.DateField(write_only=True)
    end_date = serializers.DateField(write_only=True)
    settings = serializers.JSONField(write_only=True)
    budget = BudgetRetrieveSerializer(write_only=True)


#################################################################
# Participants
#################################################################
class TripParticipantsListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['id', 'email',]


class TripParticipantsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip


#################################################################
# Ticket
#################################################################
class BaseTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'ticket', 'profile', 'trip']


class TicketCreateSerializer(BaseTicketSerializer):
    id = serializers.IntegerField(write_only=True)
    ticket = serializers.FileField()
    profile = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserProfile.objects.all())
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    def create(self, validated_data):
        view = self.context['view']
        profile = view.request.user.get_default_profile()
        validated_data['profile'] = profile
        return Ticket.objects.create(**validated_data)


class TicketRetrieveSerializer(BaseTicketSerializer):
    id = serializers.IntegerField(write_only=True)
    ticket = serializers.FileField(read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)


class TicketListSerializer(BaseTicketSerializer):
    id = serializers.IntegerField(read_only=True)
    ticket = serializers.FileField(read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)


class TicketUpdateSerializer(BaseTicketSerializer):
    id = serializers.IntegerField(write_only=True)
    ticket = serializers.FileField()
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)


class TicketDestroySerializer(BaseTicketSerializer):
    id = serializers.IntegerField(write_only=True)
    ticket = serializers.FileField(write_only=True)
    profile = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserProfile.objects.all())
    trip = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Trip.objects.all())


#################################################################
# Expense
#################################################################
class ExpenseSerializer(serializers.ModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(required=True, queryset=Trip.objects.all())
    user = serializers.PrimaryKeyRelatedField(required=True, queryset=UserProfile.objects.all())

    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'date', 'description', 'trip', 'user', 'type'
        ]
        read_only_fields = ['id']
