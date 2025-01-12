from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework import serializers

from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Hasło musi składać się z conajmniej 8 znaków.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Hasło musi zawierać co najmniej jedną liczbę.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Hasło musi zawierać co najmniej jedną literę.")
        return value

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")

        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")

        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'date_of_birth', 'password']
        extra_kwargs = {'password': {'write_only': True}}
