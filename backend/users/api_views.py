from rest_framework.generics import CreateAPIView

from users.models import CustomUser
from .serializers import RegisterSerializer


class UserCreateView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
