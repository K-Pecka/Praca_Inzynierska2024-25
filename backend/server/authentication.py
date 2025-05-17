from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from trips.models import TripAccessToken

class TripTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print('xd00')
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            print('xd01')
            return None

        parts = auth_header.split()
        if not parts:
            print('xd02')
            return None

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise AuthenticationFailed('Niepoprawny format tokenu.')
        print('xd03')
        token = parts[1]
        trip_token = TripAccessToken.objects.filter(token=token).first()
        if not trip_token:
            print('xd04')
            raise AuthenticationFailed('Niepoprawny token.')
        print('xd05')
        token_owner = trip_token.user_profile.user

        return token_owner, None

    def authenticate_header(self, request):
        return 'Bearer'
