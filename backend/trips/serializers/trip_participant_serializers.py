from rest_framework import serializers

from users.models import UserProfile


class TripParticipantsUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(required=False)
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        required=False,
        source='profile',
        help_text="Wymagane tylko dla istniejących użytkowników. Jeśli brak, traktowane jako zaproszenie gościa."
    )

    class Meta:
        fields = ['name', 'email', 'profile_id']


class JoinTripSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
