from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, UserProfile
from .serializers import UserCreateSerializer, UserUpdateSerializer, UserUpdatePasswordSerializer, UserListSerializer, \
    UserProfileListSerializer

from rest_framework import status

from django.db import transaction


@extend_schema(tags=['User'], parameters = [
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        with transaction.atomic():
            user = serializer.save()

            try:
                serializer.send_confirmation_email(user, self.request.build_absolute_uri)
            except Exception:
                transaction.set_rollback(True)
                return Response(
                    {"error": "Could not send confirmation email. Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


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
