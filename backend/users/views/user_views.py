from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from server import settings
from server.authentication import TripTokenAuthentication
from server.permissions import IsAuthenticatedOrValidTripToken
from users.serializers.user_serializers import UserCreateSerializer, UserUpdateSerializer, UserUpdatePasswordSerializer, \
    ConfirmEmailSerializer, CheckAccessSerializer, UserRetrieveSerializer

from users.models import CustomUser, UserPermission, UserProfile


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer


class UserByProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRetrieveSerializer

    def get_object(self):
        profile_pk = self.kwargs['pk']
        profile = get_object_or_404(UserProfile, pk=profile_pk)

        user = profile.user
        if not user:
            raise ValueError("Nie znaleziono użytkownika.")
        return user


class UserUpdateAPIView(UpdateAPIView):
    authentication_classes = [TripTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticatedOrValidTripToken]
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
    permission_classes = [AllowAny,]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            if user.is_guest:
                user.is_guest = False
                profile = user.get_default_profile()
                profile.type = 'tourist'
                profile.save()
            user.is_active = True
            user_profile = user.get_default_profile()
            user_profile.trip_access_tokens.all().delete()
            user.save()
            return HttpResponseRedirect(f"{settings.LOGIN_PAGE}")
        else:
            return HttpResponseRedirect(f"{settings.FAILED_REGISTRATION_PAGE}")


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

        profile = user.profiles.filter(type__name='client').first()

        if profile is None:
            return Response({"error": "Profil użytkownika nie istnieje."}, status=status.HTTP_404_NOT_FOUND)

        is_allowed, message = UserPermission.check_permission(profile, perm_code, perm_action)

        if is_allowed:
            return Response({"message": f"{message}"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"{message}"}, status=status.HTTP_403_FORBIDDEN)


@extend_schema(
    tags=['user'],
)
class CheckAccountTypeAPIView(APIView):
    """
    View to check the account type of the user.
    """
    def get(self, request):
        user = request.user
        if not user:
            raise ValueError("Nie znaleziono użytkownika.")

        profile = user.get_default_profile()
        profile_type = profile.type.name
        if not profile_type:
            raise ValueError("Profil użytkownika nie ma przypisanego typu.")

        return Response({"profile_type": profile_type}, status=status.HTTP_200_OK)


@extend_schema(tags=['user'])
class UserDeleteAPIView(DestroyAPIView):
    """
    View for handling deletion of user accounts.

    This API view is responsible for deleting user accounts. It extends the
    DestroyAPIView from Django REST framework, providing a simple way to delete a
    user account by their ID. Appropriate permissions should be used to restrict
    access to this view to authorized users only.

    @extend_schema(tags=['user'])
    """
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user