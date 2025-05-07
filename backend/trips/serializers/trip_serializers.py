from django.utils import timezone
from django.db import transaction

from rest_framework import serializers

from trips.models import Budget, Trip
from users.models import UserProfile
from users.serializers.user_profile_serializers import UserProfileListSerializer


class TripCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    creator = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), required=False)
    members = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects.all())
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    budget_amount = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)

    def validate_budget_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Kwota budżetu musi być większa od zera.")
        return value

    def validate(self, data):
        request = self.context['request']

        if not request.user.is_guide:
            if Trip.objects.filter(creator=request.user.get_default_profile()).count() > 2:
                raise serializers.ValidationError("Osiągnąłeś limit wycieczek dla swojego profilu.")

        if data.get("start_date") and data.get("end_date"):
            if data["start_date"] > data["end_date"]:
                raise serializers.ValidationError("Data rozpoczęcia nie może być późniejsza niż data zakończenia.")
            if data["start_date"] < timezone.now().date():
                raise serializers.ValidationError("Data rozpoczęcia nie może być wcześniejsza niż dzisiaj.")
        return data

    class Meta:
        model = Trip
        fields = ['id', 'name', 'creator', 'members', 'start_date', 'end_date']

    def create(self, validated_data):
        try:
            with transaction.atomic():
                request = self.context['request']
                budget_amount = validated_data.pop('budget_amount')

                if 'creator' not in validated_data:
                    validated_data['creator'] = request.user.get_default_profile()

                trip = super().create(validated_data)

                Budget.objects.create(trip=trip, amount=budget_amount)

                return trip
        except Exception as e:
            raise e

    class Meta:
        model = Trip
        fields = ['id', 'name', 'creator', 'members', 'start_date', 'end_date', 'budget_amount']


class TripRetrieveSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    creator = UserProfileListSerializer(read_only=True)
    members = UserProfileListSerializer(read_only=True, many=True)
    pending_members = serializers.SerializerMethodField()
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    activity_count = serializers.SerializerMethodField()
    budget_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    def get_pending_members(self, obj):
        access_tokens = obj.access_tokens.filter(is_pending=True)
        guest_members = [access_token.user_profile for access_token in access_tokens]
        return UserProfileListSerializer(guest_members, many=True).data

    def get_activity_count(self, obj):
        return sum(itinerary.activities.count() for itinerary in obj.itineraries.all())

    class Meta:
        model = Trip
        fields = ['name', 'creator', 'members', 'pending_members', 'start_date', 'end_date', 'activity_count', 'budget_amount']


class TripListSerializer(TripRetrieveSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    creator = UserProfileListSerializer(read_only=True)
    members = UserProfileListSerializer(read_only=True, many=True)
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    is_creator = serializers.SerializerMethodField()
    budget_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    def get_is_creator(self, obj):
        request = self.context['request']
        user_profile = request.user.get_default_profile()
        return obj.creator == user_profile

    class Meta:
        model = Trip
        fields = ['id', 'name', 'creator', 'members', 'start_date', 'end_date', 'is_creator', 'budget_amount']


class TripUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all())
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    budget_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    def validate(self, data):
        if data.get("start_date") and data.get("end_date"):
            if data["start_date"] > data["end_date"]:
                raise serializers.ValidationError("Data rozpoczęcia nie może być późniejsza niż data zakończenia.")
            if data["start_date"] < timezone.now().date():
                raise serializers.ValidationError("Data rozpoczęcia nie może być wcześniejsza niż dzisiaj.")
            return data

    class Meta:
        model = Trip
        fields = ['id', 'name', 'creator', 'members', 'start_date', 'end_date', 'budget_amount']


class TripDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        read_only_fields = ['id']
