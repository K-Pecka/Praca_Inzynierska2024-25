from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

from users.models import CustomUser, UserPermission

User = get_user_model()


def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/confirmation_success.html')
    else:
        return render(request, 'registration/confirmation_failed.html')


def check_access(request, user_pk, perm_code, perm_action):
    user = CustomUser.objects.get(pk=user_pk)
    profile = user.profiles.filter(type='client').first()

    if profile is None:
        return Response({"error": "Profil użytkownika nie istnieje."}, status=status.HTTP_404_NOT_FOUND)

    permission_check = UserPermission.check_permission(profile, perm_code, perm_action)
    if permission_check:
        return Response({"message": "Dostęp do akcji został przyznany."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Brak odpowiednich uprawnień do wykonania akcji."}, status=status.HTTP_403_FORBIDDEN)
