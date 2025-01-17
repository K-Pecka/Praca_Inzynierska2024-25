from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserCreateSerializer, UserUpdateSerializer, UserUpdatePasswordSerializer


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
