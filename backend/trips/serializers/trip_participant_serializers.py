from rest_framework import serializers

from trips.serializers.trip_serializers import BaseTripSerializer

from trips.serializers.budget_serializers import BudgetRetrieveSerializer

from users.models import CustomUser
from users.serializers.user_profile_serializers import UserProfileListSerializer


class TripParticipantsUpdateSerializer(BaseTripSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = UserProfileListSerializer(read_only=True, many=True)
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    settings = serializers.JSONField(read_only=True)
    budget = BudgetRetrieveSerializer(read_only=True)

    def get_budget(self, obj):
        return obj.budget


class InvitationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    date = serializers.DateTimeField()
    email = serializers.EmailField()
    is_guest = serializers.BooleanField(default=False)
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)


class JoinTripSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
