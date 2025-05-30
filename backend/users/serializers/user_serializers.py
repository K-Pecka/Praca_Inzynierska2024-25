from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http.response import HttpResponseRedirect

from django.db import transaction
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

from rest_framework import serializers

from users.models import CustomUser


class UserRetrieveSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']


class UserListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']


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

        existing_user = CustomUser.objects.filter(email=value).first()
        if existing_user and not existing_user.is_guest:
            raise serializers.ValidationError("Użytkownik o podanym adresie email już istnieje.")

        return value

    def create(self, validated_data):
        validated_data['is_active'] = False
        validated_data['password'] = make_password(validated_data['password'])

        with transaction.atomic():
            user, created = CustomUser.objects.get_or_create(
                email=validated_data['email'],
                defaults=validated_data
            )

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            confirmation_link = self.context['request'].build_absolute_uri(
                f"/user/confirm-email/{uidb64}/{token}/"
            )
            try:
                self.send_confirmation_email(user, confirmation_link)
            except Exception as e:
                raise serializers.ValidationError({"error": f"Błąd przy tworzeniu użytkownika {e}"})

            return user

    def send_confirmation_email(self, user, confirmation_link):
        subject = 'Potwierdź swój adres email.'
        message = render_to_string('emails/confirmation_email.html', {
            'user': user,
            'confirmation_link': confirmation_link,
        })
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': []},
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    password_confirm = serializers.CharField(write_only=True, required=False)

    def validate(self, data):
        password = data.get('password')
        password_confirm = self.initial_data.get('password_confirm')
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                raise serializers.ValidationError(e.messages)
        if password or password_confirm:
            if password != password_confirm:
                raise serializers.ValidationError("Hasła muszą być takie same.")
            if password and len(password) < 8:
                raise serializers.ValidationError("Hasło musi mieć co najmniej 8 znaków.")
        data.pop('password_confirm', None)
        return data

    def update(self, instance, validated_data):
        if instance.is_guest:
            password = validated_data.get('password', None)
            if not password:
                raise serializers.ValidationError("Podanie hasła jest wymagane.")
            if not validated_data.get("first_name"):
                raise serializers.ValidationError("Podanie imienia jest wymagane.")
            return instance.register_guest_account(validated_data)

        password = validated_data.pop('password', None)

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        if password:
            instance.set_password(password)
            instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'password', 'password_confirm']
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


class ConfirmEmailSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()


class CheckAccessSerializer(serializers.Serializer):
    user_pk = serializers.IntegerField()
    perm_code = serializers.CharField()
    perm_action = serializers.CharField()
