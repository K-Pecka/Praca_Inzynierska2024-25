from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from trips.models import TripAccessToken

class TripTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        parts = auth_header.split()
        if not parts:
            return None

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise AuthenticationFailed('Niepoprawny format tokenu.')
        token = parts[1]
        trip_token = TripAccessToken.objects.filter(token=token).first()
        if not trip_token:
            raise AuthenticationFailed('Niepoprawny token.')
        token_owner = trip_token.user_profile.user

        return token_owner, None

    def authenticate_header(self, request):
        return 'Bearer'
