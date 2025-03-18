from rest_framework import serializers

from trips.models import Budget, Trip
from trips.serializers.budget_serializers import BudgetRetrieveSerializer
from users.models import UserProfile
from users.serializers.user_profile_serializers import UserProfileListSerializer


class BaseTripSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    creator = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), required=False)
    members = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=UserProfile.objects.all())
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    settings = serializers.JSONField(required=False)
    budget = serializers.PrimaryKeyRelatedField(queryset=Budget.objects.all(), required=False)

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
    members = UserProfileListSerializer(read_only=True, many=True)
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    settings = serializers.JSONField(read_only=True)
    budget = BudgetRetrieveSerializer(read_only=True)

    def get_budget(self, obj):
        return obj.budget


class TripListSerializer(TripRetrieveSerializer):
    id = serializers.IntegerField(read_only=True)
    members = UserProfileListSerializer(read_only=True, many=True)


class TripUpdateSerializer(BaseTripSerializer):
    id = serializers.IntegerField(read_only=True)
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
