from urllib.parse import urlencode

from django.contrib.auth import login
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from server.permissions import IsTripCreator
from trips.models import Trip, TripAccessToken
from trips.serializers.trip_participant_serializers import TripParticipantsUpdateSerializer, InvitationSerializer
from users.models import UserProfile, CustomUser


@extend_schema(tags=['trip'], parameters=[
    OpenApiParameter(
        name='action',
        description='Action to add or remove user from the trip (add/remove)',
        required=True,
        type=str,
        enum=['add', 'remove'], )
])
class TripParticipantsUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripParticipantsUpdateSerializer

    def get_object(self):
        return get_object_or_404(Trip, id=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        trip = self.get_object()
        action = self.request.query_params.get('action', None)
        profile_id = kwargs.get('profile_pk')
        user_profile = get_object_or_404(UserProfile, id=profile_id)

        if not self.validate_action(action):
            return Response({"detail": "Niepoprawna akcja, dostępne opcje to 'add' lub 'remove'."}, status=400)

        if action == 'add':
            return Trip.add_member(trip, user_profile)
        elif action == 'remove':
            return Trip.remove_member(trip, user_profile)

    def validate_action(self, action):
        return action in ['add', 'remove']

@extend_schema(
    tags=['trip invitation'],
    request=InvitationSerializer,
    responses={
        200: OpenApiResponse(description="Zaproszenie wysłane!"),
        400: OpenApiResponse(description="Niepoprawne dane zaproszenia."),
        404: OpenApiResponse(description="Trip not found."),
        500: OpenApiResponse(description="Server error while sending invitation email.")
    }
)
class InviteUserAPIView(APIView):
    def post(self, request, trip_id):
        serializer = InvitationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": "Niepoprawne dane zaproszenia."}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            if data.get('is_guest'):
                try:
                    user = CustomUser.create_guest_account(data['name'], data['email'])
                except ValueError as e:
                    return Response(
                        {"error": str(e)},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                user = data.get('user')
                if not user:
                    return Response(
                        {"error": "User is required when not a guest"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            trip = Trip.objects.get(id=trip_id)
            invitation_link = self.create_invitation_link(trip, user)
            self.send_trip_invitation_email(data, invitation_link, trip)

            return Response(
                {"message": "Zaproszenie wysłane!", "invitation_link": invitation_link},
                status=status.HTTP_200_OK
            )

        except Trip.DoesNotExist:
            return Response(
                {"error": "Wycieczka nie istnieje."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response(
                {"error": "Wystąpił błąd podczas przetwarzania zaproszenia"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create_invitation_link(self, trip, user):
        token = TripAccessToken.generate_token()
        try:
            user_profile = user.get_default_profile()

            token_instance, created = TripAccessToken.objects.get_or_create(
                trip=trip,
                user_profile=user_profile,
                defaults={'token': token}
            )

            query_params = urlencode({'token': token})
            invitation_link = f"{settings.API_URL}{reverse('trip_join')}?{query_params}"

            if not created:
                token_instance.token = token
                token_instance.save()

            return invitation_link

        except UserProfile.DoesNotExist:
            raise Exception('Nie znaleziono profilu użytkownika')
        except Exception as e:
            raise ValueError(f"Błąd generowania linku: {str(e)}")

    def send_trip_invitation_email(self, data, invitation_link, trip):
        subject = 'Zaproszenie do wycieczki Plannder'
        html_message = render_to_string('emails/trip_invitation_email.html', {
            'name': data['name'],
            'trip_name': trip.name,
            'date': data['date'],
            'trip_link': invitation_link
        })
        plain_message = strip_tags(html_message)

        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[data['email']],
                html_message=html_message,
            )
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")



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
class JoinTripAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
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
