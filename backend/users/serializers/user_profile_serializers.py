from rest_framework import serializers

from users.models import UserProfile, UserProfileType


class UserProfileListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True
    )
    type = serializers.PrimaryKeyRelatedField(
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
    type = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    is_default = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = UserProfile
        fields = ['id', 'type', 'is_default']


class UserProfileCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=UserProfile.objects.all(),
    )
    type = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=UserProfileType.objects.all()
    )
    is_default = serializers.BooleanField(
        read_only=True,
    )

    def create(self, validated_data):
        kwargs = self.context.get('kwargs')
        user = kwargs.get('user')
        if not user:
            raise serializers.ValidationError("Nie przekazano id użytkownika.")

        user_profile = UserProfile.objects.create(
            user=user,
            type=validated_data['type'],
        )
        return user_profile

    class Meta:
        model = UserProfile
        fields = ['user', 'type', 'is_default']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True
    )
    type = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=UserProfileType.objects.all(

        ))
    is_default = serializers.BooleanField(
        write_only=True
    )

    class Meta:
        model = UserProfile
        fields = ['id', 'type', 'is_default']
