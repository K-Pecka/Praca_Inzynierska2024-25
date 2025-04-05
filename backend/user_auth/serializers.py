from typing import Dict, Any

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(max_length=255, read_only=True)
    email = serializers.EmailField(max_length=255, read_only=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        profile = user.get_default_profile()

        token['profile_id'] = profile.id if profile else None
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['fullname'] = user.full_name
        token['email'] = user.email

        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        profile = self.user.get_default_profile()

        data['profile_id'] = profile.id if profile else None
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['fullname'] = self.user.full_name
        data['email'] = self.user.email

        return data
