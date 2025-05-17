<<<<<<< Updated upstream
from django.utils import timezone
from django.db import transaction
=======
from datetime import date
>>>>>>> Stashed changes

from rest_framework import serializers

from trips.models import Trip
from users.models import UserProfile
from users.serializers.user_profile_serializers import UserProfileListSerializer


<<<<<<< Updated upstream
class TripCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    creator = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), required=False)
    members = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects.all())
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    budget_amount = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)

    def validate_budget_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Kwota budżetu nie może być ujemna.")
        return value

    def validate(self, data):
        request = self.context['request']
=======
class BaseTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'name', 'creator', 'members', 'budget', 'start_date', 'end_date']


class TripCreateSerializer(BaseTripSerializer):
    name = serializers.CharField()
    creator = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    members = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects.all())
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    budget = serializers.DecimalField(max_digits=7, decimal_places=2, required=True)

    def validate(self, data):
        request = self.context['request']
        members = data.get("members", [])
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)
>>>>>>> Stashed changes

        if not request.user.is_guide:
            if Trip.objects.filter(creator=request.user.get_default_profile()).count() > 2:
                raise serializers.ValidationError("Osiągnąłeś limit wycieczek dla swojego profilu.")

<<<<<<< Updated upstream
        if data.get("start_date") and data.get("end_date"):
            if data["start_date"] > data["end_date"]:
                raise serializers.ValidationError("Data rozpoczęcia nie może być późniejsza niż data zakończenia.")
            if data["start_date"] < timezone.now().date():
                raise serializers.ValidationError("Data rozpoczęcia nie może być wcześniejsza niż dzisiaj.")
=======
        if start_date < date.today():
            raise serializers.ValidationError("Data rozpoczęcia nie może być wcześniejsza niż dzisiejsza data.")

        if start_date > end_date:
            raise serializers.ValidationError("Data zakończenia musi być późniejsza niż data rozpoczęcia.")

        if members and data.get("creator") in members:
            raise serializers.ValidationError("Właściciel nie może być uczestnikiem wycieczki.")
>>>>>>> Stashed changes
        return data

    def create(self, validated_data):
        try:
<<<<<<< Updated upstream
            with transaction.atomic():
                request = self.context['request']

                if 'creator' not in validated_data:
                    validated_data['creator'] = request.user.get_default_profile()

                trip = super().create(validated_data)

                return trip
=======
            request = self.context['request']
            validated_data['creator'] = request.user.get_default_profile()
            budget_amount = validated_data.pop('budget', None)
            trip = super().create(validated_data)
            Budget.objects.create(currency='PLN', trip=trip, amount=budget_amount)
            return trip
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    activity_count = serializers.SerializerMethodField()
    budget_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
=======
    budget = BudgetRetrieveSerializer(read_only=True)
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
    budget_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

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
=======
    budget = BudgetRetrieveSerializer()
    # TODO: walidacja start_date end_date czy mozna zmienic


class TripDestroySerializer(BaseTripSerializer):
    id = serializers.IntegerField(write_only=True)
    name = serializers.CharField(write_only=True)
    creator = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserProfile.objects.all())
    members = serializers.PrimaryKeyRelatedField(write_only=True, many=True, queryset=UserProfile.objects.all())
    start_date = serializers.DateField(write_only=True)
    end_date = serializers.DateField(write_only=True)
    budget = BudgetRetrieveSerializer(write_only=True)
>>>>>>> Stashed changes
