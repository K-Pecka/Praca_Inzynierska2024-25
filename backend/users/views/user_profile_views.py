from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import UserProfile
from users.serializers.user_profile_serializers import UserProfileListSerializer, UserProfileUpdateSerializer, \
    UserProfileCreateSerializer, UserChangeProfileSerializer


@extend_schema(tags=['profile'], parameters = [
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
            return UserProfile.objects.filter(user__email__icontains=search_query, type='tourist')
        else:
            return UserProfile.objects.all()


@extend_schema(tags=['profile'])
class UserProfileUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileUpdateSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['profile'])
class UserProfileCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileCreateSerializer


@extend_schema(tags=['profile'])
class ChangeDefaultUserProfileView(UpdateAPIView):
    serializer_class = UserChangeProfileSerializer
    permission_classes = [IsAuthenticated]

