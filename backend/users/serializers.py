from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode

from rest_framework import serializers

from users.models import CustomUser


class UserListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    date_of_birth = serializers.DateField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'date_of_birth']


class UserCreateSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
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
        validated_data['is_active'] = False

        validated_data['password'] = make_password(validated_data['password'])

        user = super().create(validated_data)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        confirmation_link = self.context['request'].build_absolute_uri(
            f"/confirm-email/{uid}/{token}/"
        )

        try:
            self.send_confirmation_email(user, confirmation_link)
        except Exception:
            raise serializers.ValidationError({"error": "User could not be created."})

        return user

    def send_confirmation_email(self, user, confirmation_link):
        subject = 'Confirm your email address'
        message = render_to_string('emails/confirmation_email.html', {
            'user': user,
            'confirmation_link': confirmation_link,
        })
        send_mail(subject, message, 'plannder@op.pl', [user.email])

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'date_of_birth', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'date_of_birth']
        read_only_fields = ['id']


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = ['id', 'password']
        read_only_fields = ['id']
