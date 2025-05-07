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
    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True
    )
    last_name = serializers.CharField(
        source="user.last_name",
        read_only=True
    )

    class Meta:
        model = UserProfile
        fields = ['id', 'type', 'email', 'first_name', 'last_name']


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
    type = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=UserProfileType.objects.all()
    )
    is_default = serializers.BooleanField(required=False)

    class Meta:
        model = UserProfile
        fields = ['type', 'is_default']

    def create(self, validated_data):
        user = self.context['request'].user
        is_default = validated_data.pop('is_default', False)

        if is_default:
            UserProfile.objects.filter(user=user).update(is_default=False)
        else:
            has_default = UserProfile.objects.filter(user=user, is_default=True).exists()
            if not has_default:
                is_default = True

        return UserProfile.objects.create(
            user=user,
            is_default=is_default,
            **validated_data
        )


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.PrimaryKeyRelatedField(
        queryset=UserProfileType.objects.all(),
        required=False
    )
    is_default = serializers.BooleanField(required=False)

    class Meta:
        model = UserProfile
        fields = ['id', 'type', 'is_default']

    def update(self, instance, validated_data):
        if validated_data.get('is_default') is True:
            UserProfile.objects.filter(
                user=instance.user
            ).exclude(pk=instance.pk).update(is_default=False)

        return super().update(instance, validated_data)
