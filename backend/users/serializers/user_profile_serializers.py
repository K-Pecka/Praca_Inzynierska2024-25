from django.db import transaction

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
    id = serializers.IntegerField(read_only=True)
    type = serializers.PrimaryKeyRelatedField(
        queryset=UserProfileType.objects.all()
    )
    is_default = serializers.BooleanField(required=False)

    class Meta:
        model = UserProfile
        fields = ['id', 'type', 'is_default']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        if len(user.profiles) == 2:
            raise serializers.ValidationError("Użytkownik nie może stworzyć więcej profili.")

        if user.is_guest:
            raise serializers.ValidationError("Gość nie może tworzyć nowych kont.")

        return UserProfile.objects.create(**validated_data)


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


class UserChangeProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.PrimaryKeyRelatedField(
        read_only=True,
        required=False
    )
    is_default = serializers.BooleanField(read_only=True, required=False)

    def update(self, instance, validated_data):
        request = self.context['request']

        exclude_profile_type = UserProfileType.objects.get(code='guest')

        profiles = request.user.profiles.filter(user__is_active=True).exclude(type=exclude_profile_type)
        if len(profiles) < 2:
            raise serializers.ValidationError("Użytkownik posiada tylko jeden aktywny profil.")

        with transaction.atomic():
            for profile in profiles:
                profile.is_default = not profile.is_default
                profile.save()

        return request.user.get_default_profile()

    class Meta:
        model = UserProfile
        fields = ['id', 'type', 'is_default']