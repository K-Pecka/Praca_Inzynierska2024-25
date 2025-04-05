from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user_auth.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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
        except Exception as e: # TODO: potencjał na log
            return Response({"detail": "Wystąpił błąd podczas wylogowywania."}, status=status.HTTP_400_BAD_REQUEST)
