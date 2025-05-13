from rest_framework import serializers

from users.models import UserProfile


class TripParticipantsUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        required=False,
        source='profile',
        help_text="Wymagane tylko dla istniejących użytkowników. Jeśli brak, traktowane jako zaproszenie gościa."
    )

    class Meta:
        fields = ['email', 'profile_id']


class JoinTripSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
