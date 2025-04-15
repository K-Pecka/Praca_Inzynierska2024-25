from rest_framework import serializers

from users.models import UserProfile, UserProfileType
from users.serializers.user_profile_type_serializers import UserProfileTypeRetrieveSerializer


class UserProfileListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True
    )
    type = UserProfileTypeRetrieveSerializer(
        read_only=True
    )
    email = serializers.EmailField(
        source='user.email'
    )

    class Meta:
        model = UserProfile
        fields = ['id', 'type', 'email',]


class UserProfileListJWTSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True
    )
    type = UserProfileTypeRetrieveSerializer(
        read_only=True
    )
    is_default = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = UserProfile
        fields = ['id', 'type', 'is_default']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=UserProfileType.objects.all(

        ))
    is_default = serializers.BooleanField(
        write_only=True
    )

    class Meta:
        model = UserProfile
        fields = ['type', 'is_default']
