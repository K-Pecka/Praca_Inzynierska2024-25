from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db import transaction

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import status
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from server.permissions import IsTripCreator
from trips.models import Trip, TripAccessToken
from trips.serializers.trip_participant_serializers import TripParticipantsUpdateSerializer
from users.models import CustomUser, UserProfile


def delete_access_token(trip, profile):
    token = TripAccessToken.objects.filter(trip=trip, user_profile=profile).first()

    if token:
        token.delete()


def handle_remove(trip, data):
    profile = data.get('profile')
    if not profile:
        raise ValidationError(_("Nie podano profilu użytkownika do usunięcia"))

    if trip.check_if_is_member(profile) or trip.check_if_is_pending(profile):
        if profile.type.code == 'guest':
            with transaction.atomic():
                profile.user.delete()
        else:
            with transaction.atomic():
                trip.members.remove(profile)
        delete_access_token(trip, profile)

        if not trip.check_if_is_member(profile) or trip.check_if_is_pending(profile):
            return Response({"message": _("Użytkownik został pomyślnie usunięty z wycieczki")})

    return Response({
        "message": _("Użytkownik nie był przypisany do tej wycieczki lub już został usunięty."),
    })


def send_invitation_email(name, email, trip, invitation_link):
    subject = f"{_('Zaproszenie do wycieczki')} {trip.name}"
    html_message = render_to_string('emails/trip_invitation_email.html', {
        'name': name,
        'trip_name': trip.name,
        'start_date': trip.start_date,
        'end_date': trip.end_date,
        'trip_link': invitation_link
    })
    sent_count = send_mail(
        subject=subject,
        message=strip_tags(html_message),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message
    )

    if sent_count == 0:
        raise Exception("Nie udało się wysłać e-maila z zaproszeniem.")


@extend_schema(
    tags=['trip invitation'],
    parameters=[
        OpenApiParameter(
            name='action',
            description='Action to perform (invite/remove)',
            required=True,
            type=str,
            enum=['invite', 'remove'],
            location="query"
        )
    ],
    responses={
        200: {"description": f"{_('Operacja wykonana pomyślnie')}"},
        400: {"description": f"{_('Niepoprawne dane wejściowe')}"},
        403: {"description": f"{_('Brak uprawnień')}"},
        404: {"description": f"{_('Nie znaleziono wycieczki lub użytkownika')}"},
        500: {"description": f"{_('Błąd serwera')}"}
    }
)
class TripParticipantsUpdateAPIView(UpdateAPIView):
    serializer_class = TripParticipantsUpdateSerializer
    permission_classes = [IsAuthenticated, IsTripCreator]

    def get_object(self):
        return Trip.objects.get(pk=self.kwargs['trip_pk'])

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
                return handle_remove(trip, data)
            return None
        except Exception as e:
            return Response(
                {"error": e},
                status=status.HTTP_400_BAD_REQUEST
            )

    def handle_invite(self, trip, data):
        user = CustomUser.objects.filter(email=data['email']).first()

        if user == self.request.user:
            raise ValidationError(_("Nie możesz zaprosić samego siebie"))

        if trip.members.count() >= 5:
            raise ValidationError(_("Wycieczka może mieć maksymalnie 5 uczestników."))

        if not CustomUser.objects.filter(email=data['email']).exists():
            try:
                user = CustomUser.create_guest_account(
                        data['name'],
                        data['email']
                )
            except Exception as e:
                raise ValidationError(_("Nie udało się utworzyć konta gościa. Sprawdź poprawność danych. {e}".format(e=str(e))))

            profile = user.get_default_profile()
        else:
            profile = UserProfile.objects.filter(user=user, type__code='tourist').first()

            if not profile:
                raise ValidationError(_("Użytkownik o podanym mailu nie posiada konta turysty"))

            if profile.type.code == 'guide':
                raise ValidationError(_("Nie można dodać przewodnika do wycieczki."))

        if trip.members.filter(id=profile.id).exists():
            raise ValidationError(_("Użytkownik już jest uczestnikiem wycieczki"))

        invitation_link = self.create_invitation_link(trip, profile.user)

        send_invitation_email(
            name=data.get('name', profile.user.full_name),
            email=data.get('email', profile.user.email),
            trip=trip,
            invitation_link=invitation_link
        )

        return Response({
            "message": f"{_('Zaproszenie wysłane')}",
            "invitation_link": invitation_link,
            "is_guest": 'profile' not in data
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


def get_trip_access_token(token):
    return TripAccessToken.objects.filter(token=token).get()


@extend_schema(
    tags=['trip invitation'],
    parameters=[OpenApiParameter("token", str, description="Token dostępu do wycieczki", required=True)],
    responses={
        200: OpenApiResponse(description=f"{_('Użytkownik dołączył do wycieczki!')}"),
        400: OpenApiResponse(description=f"{_('Brak tokenu w linku.')}"),
        404: OpenApiResponse(description=f"{_('Podany token nie istnieje.')}"),
        403: OpenApiResponse(description=f"{_('Konto użytkownika jest nieaktywne.')}"),
        500: OpenApiResponse(description=f"{_('Nie udało się zalogować.')}")
    }
)
class JoinTripAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        token = request.GET.get('token')

        if not token:
            return Response({'error': f'{_()}Brak tokenu w linku.'}, status=status.HTTP_400_BAD_REQUEST)

        trip_access_token = get_trip_access_token(token)
        if not trip_access_token:
            return Response({'error': f'{_()}Podany token nie istnieje.'}, status=status.HTTP_404_NOT_FOUND)

        user_profile = trip_access_token.user_profile
        user = user_profile.user

        if not user.is_active:
            return Response({"error": f"{_('Konto użytkownika jest nieaktywne.')}"}, status=status.HTTP_403_FORBIDDEN)
        try:
            Trip.add_member(trip_access_token.trip, user_profile)
            trip_access_token.change_status()
        except Exception as e:
            return Response({"error": f"{_('Nie udało się dodać użytkownika do wycieczki:')} {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        return HttpResponseRedirect(f"{settings.TRIP_JOINING_PAGE}?token={token}")
