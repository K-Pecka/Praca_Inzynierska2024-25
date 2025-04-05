from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import status
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from server.permissions import IsTripCreator
from trips.models import Trip, TripAccessToken
from trips.serializers.trip_participant_serializers import TripParticipantsUpdateSerializer
from users.models import CustomUser


@extend_schema(
    tags=['trip invitation'],
    parameters=[
        OpenApiParameter(
            name='action',
            description='Action to perform (invite/remove)',
            required=True,
            type=str,
            enum=['invite', 'remove'],
            location=OpenApiParameter.QUERY
        )
    ],
    responses={
        200: {"description": "Operacja wykonana pomyślnie"},
        400: {"description": "Niepoprawne dane wejściowe"},
        403: {"description": "Brak uprawnień"},
        404: {"description": "Nie znaleziono wycieczki lub użytkownika"},
        500: {"description": "Błąd serwera"}
    }
)
class TripParticipantsUpdateAPIView(UpdateAPIView):
    serializer_class = TripParticipantsUpdateSerializer
    permission_classes = [IsAuthenticated, IsTripCreator]

    def get_object(self):
        return get_object_or_404(Trip, pk=self.kwargs['trip_id'])

    def update(self, request, *args, **kwargs):
        trip = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        action = self.request.query_params.get('action', None)

        try:
            if action == 'invite':
                return self.handle_invite(trip, data)
            elif action== 'remove':
                return self.handle_remove(trip, data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def handle_invite(self, trip, data):
        if 'profile' not in data:
            user = CustomUser.create_guest_account(
                data['name'],
                data['email']
            )
            profile = user.get_default_profile()
        else:
            profile = data['profile']

        if trip.members.filter(id=profile.id).exists():
            raise ValidationError("Użytkownik już jest uczestnikiem wycieczki")

        invitation_link = self.create_invitation_link(trip, profile.user)

        self.send_invitation_email(
            name=data.get('name', profile.user.full_name),
            email=data.get('email', profile.user.email),
            trip=trip,
            invitation_link=invitation_link
        )

        return Response({
            "message": "Zaproszenie wysłane",
            "invitation_link": invitation_link,
            "is_guest": 'profile' not in data
        })

    def handle_remove(self, trip, data):
        if 'profile' not in data:
            raise ValidationError("profile_id jest wymagane do usunięcia")

        profile = data['profile']
        if not trip.members.filter(id=profile.id).exists():
            raise ValidationError("Użytkownik nie jest uczestnikiem tej wycieczki")

        trip.members.remove(profile)
        return Response({
            "message": "Użytkownik został usunięty z wycieczki",
            "removed_profile_id": profile.id
        })

    def create_invitation_link(self, trip, user):
        token = TripAccessToken.generate_token()
        token_instance, _ = TripAccessToken.objects.update_or_create(
            trip=trip,
            user_profile=user.get_default_profile(),
            defaults={'token': token}
        )
        endpoint_path = reverse('trip_join')
        return f"{self.request.build_absolute_uri(endpoint_path)}?token={token}"

    def send_invitation_email(self, name, email, trip, invitation_link):
        subject = f"Zaproszenie do wycieczki {trip.name}"
        html_message = render_to_string('emails/trip_invitation_email.html', {
            'name': name,
            'trip_name': trip.name,
            'start_date': trip.start_date,
            'end_date': trip.end_date,
            'trip_link': invitation_link
        })
        send_mail(
            subject=subject,
            message=strip_tags(html_message),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message
        )


@extend_schema(
    tags=['trip invitation'],
    parameters=[OpenApiParameter("token", str, description="Token dostępu do wycieczki", required=True)],
    responses={
        200: OpenApiResponse(description="Użytkownik dołączył do wycieczki!"),
        400: OpenApiResponse(description="Brak tokenu w linku."),
        404: OpenApiResponse(description="Podany token nie istnieje."),
        403: OpenApiResponse(description="Konto użytkownika jest nieaktywne."),
        500: OpenApiResponse(description="Nie udało się zalogować.")
    }
)
class JoinTripAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        token = request.GET.get('token')

        if not token:
            return Response({'error': 'Brak tokenu w linku.'}, status=status.HTTP_400_BAD_REQUEST)

        trip_access_token = self.get_trip_access_token(token)
        if not trip_access_token:
            return Response({'error': 'Podany token nie istnieje.'}, status=status.HTTP_404_NOT_FOUND)

        user_profile = trip_access_token.user_profile
        user = user_profile.user

        if not user.is_active:
            return Response({'error': 'Konto użytkownika jest nieaktywne.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            Trip.add_member(trip_access_token.trip, user_profile)
        except Exception as e:
            return Response({'error': f'Nie udało się dodać użytkownika do wycieczki: {str(e)}'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            login(request, user)
        except Exception as e:
            return Response({'error': f'Nie udało się zalogować użytkownika: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Użytkownik dołączył do wycieczki!"})

    def get_trip_access_token(self, token):
        return TripAccessToken.objects.filter(token=token).get()
