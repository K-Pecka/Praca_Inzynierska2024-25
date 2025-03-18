from rest_framework import serializers

from users.models import UserProfile


class UserProfileListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['id', 'email',]
