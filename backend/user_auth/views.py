from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import PermissionDenied

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user_auth.serializers import CustomTokenObtainPairSerializer
from users.models import CustomUser


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            try:
                user_instance = CustomUser.objects.get(email=email)

                if user_instance.is_guest:
                    raise PermissionDenied("Nie możesz zalogować się jako gość.")
            except CustomUser.DoesNotExist:
                raise PermissionDenied("Niepoprawne dane logowania.")

        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    """
    Invalidate JWT tokens (log out).
    """

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Wylogowano pomyślnie."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Wystąpił błąd podczas wylogowywania."}, status=status.HTTP_400_BAD_REQUEST)
