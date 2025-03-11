from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserCreateSerializer, UserUpdateSerializer, UserUpdatePasswordSerializer

from rest_framework import status

from django.db import transaction


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
