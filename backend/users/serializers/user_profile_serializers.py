from rest_framework import serializers

from users.models import UserProfile


class UserProfileListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['id', 'email',]


class UserProfileListJWTSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(read_only=True)
    is_default = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'type', 'is_default']
