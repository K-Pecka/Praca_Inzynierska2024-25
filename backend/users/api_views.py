from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from rest_framework import status

from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import OpenApiParameter, extend_schema

from .models import UserProfile, CustomUser, UserPermission
from .serializers import UserCreateSerializer, UserUpdateSerializer, UserUpdatePasswordSerializer, UserListSerializer, \
    UserProfileListSerializer, ConfirmEmailSerializer, CheckAccessSerializer


@extend_schema(tags=['user'], parameters = [
    OpenApiParameter(
        name='email',
        description="Search users by email",
        required=False, type=str)
])
class UserProfileListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('email', None)
        if search_query:
            return UserProfile.objects.filter(user__email__icontains=search_query, type='client')
        else:
            return UserProfile.objects.all()


class UserCreateAPIView(CreateAPIView):
    permission_classes = []
    serializer_class = UserCreateSerializer


class UserUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user


class UserUpdatePasswordAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdatePasswordSerializer

    def get_object(self):
        return self.request.user


@extend_schema(
    tags=['user'],
    request=ConfirmEmailSerializer,
    responses={
        200: 'Email confirmed successfully.',
        400: 'Invalid token or user ID.'
    }
)
class ConfirmEmailView(APIView):
    """
    View to confirm the user's email address via the provided uidb64 and token.
    """
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'registration/confirmation_success.html')
        else:
            return render(request, 'registration/confirmation_failed.html')


@extend_schema(
    tags=['user'],
    request=CheckAccessSerializer,
    responses={
        200: 'Permission granted.',
        400: 'Invalid input parameters.',
        404: 'User profile not found.',
        403: 'Permission denied.'
    }
)
class CheckAccessView(APIView):
    """
    View to check user access permissions for a specific action.
    """
    def get(self, request, user_pk, perm_code, perm_action):
        try:
            user = CustomUser.objects.get(pk=user_pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "Użytkownik nie istnieje."}, status=status.HTTP_404_NOT_FOUND)

        profile = user.profiles.filter(type='client').first()

        if profile is None:
            return Response({"error": "Profil użytkownika nie istnieje."}, status=status.HTTP_404_NOT_FOUND)

        is_allowed, message = UserPermission.check_permission(profile, perm_code, perm_action)

        if is_allowed:
            return Response({"message": f"{message}"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"{message}"}, status=status.HTTP_403_FORBIDDEN)
