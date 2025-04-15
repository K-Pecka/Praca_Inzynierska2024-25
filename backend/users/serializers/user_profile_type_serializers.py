from rest_framework import serializers

from users.models import UserProfileType


class UserProfileTypeRetrieveSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True, max_length=16)
    name = serializers.CharField(read_only=True, max_length=32)

    class Meta:
        model = UserProfileType
        fields = ['code', 'name']


class UserProfileTypeListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(read_only=True, max_length=16)
    name = serializers.CharField(read_only=True, max_length=32)

    class Meta:
        model = UserProfileType
        fields = ['id', 'code', 'name']
