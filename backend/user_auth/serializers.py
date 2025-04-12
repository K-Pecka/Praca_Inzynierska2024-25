from typing import Dict, Any

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.serializers.user_profile_serializers import UserProfileListJWTSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(max_length=255, read_only=True)
    email = serializers.EmailField(max_length=255, read_only=True)
    profiles = serializers.SerializerMethodField()

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        profiles_data = UserProfileListJWTSerializer(user.profiles.all(), many=True).data

        token['profiles'] = profiles_data
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_guest'] = user.is_guest
        token['fullname'] = user.full_name
        token['email'] = user.email

        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        profiles_data = UserProfileListJWTSerializer(self.user.profiles.all(), many=True).data

        data['profiles'] = profiles_data
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['is_guest'] = self.user.is_guest
        data['fullname'] = self.user.full_name
        data['email'] = self.user.email

        return data
