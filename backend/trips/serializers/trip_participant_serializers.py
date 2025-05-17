from rest_framework import serializers

from users.models import UserProfile


<<<<<<< Updated upstream
class TripParticipantsUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        required=False,
        source='profile',
        help_text="Wymagane tylko dla istniejących użytkowników. Jeśli brak, traktowane jako zaproszenie gościa."
    )
=======
class TripParticipantsUpdateSerializer(BaseTripSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    members = UserProfileListSerializer(read_only=True, many=True)
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    budget = BudgetRetrieveSerializer(read_only=True)
>>>>>>> Stashed changes

    class Meta:
        fields = ['email', 'profile_id']


class JoinTripSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
