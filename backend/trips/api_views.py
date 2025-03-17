from django.contrib.auth import login
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from urllib.parse import urlencode

from users.models import UserProfile, CustomUser
from .models import Trip, Ticket, Budget, Expense, TripAccessToken
from .serializers import (
    TripCreateSerializer, ExpenseSerializer,
    TicketCreateSerializer, TicketUpdateSerializer, TicketRetrieveSerializer, TicketDestroySerializer,
    TicketListSerializer, TripRetrieveSerializer, TripListSerializer, TripUpdateSerializer, TripDestroySerializer,
    BudgetUpdateSerializer, BudgetDestroySerializer, TripParticipantsUpdateSerializer, InvitationSerializer,
)

from server.permissions import IsTripParticipant, IsTripCreator, IsTicketOwner


#############################################################################
# Trip
#############################################################################

@extend_schema(tags=['trip'])
class TripCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripCreateSerializer


@extend_schema(tags=['trip'])
class TripRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripRetrieveSerializer

    def get_object(self):
        id = self.kwargs['pk']
        return Trip.objects.by_id(id)


@extend_schema(tags=['trip'])
class TripListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripListSerializer

    def get_queryset(self):
        user = self.request.user.get_default_profile()
        return Trip.objects.by_user(user).select_related('creator').prefetch_related('members')


@extend_schema(tags=['trip'])
class TripUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripUpdateSerializer

    def get_object(self):
        id = self.kwargs['pk']
        return Trip.objects.by_id(id)


@extend_schema(tags=['trip'])
class TripDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripDestroySerializer

    def get_object(self):
        id = self.kwargs['pk']
        return Trip.objects.by_id(id)


#############################################################################
# Participants
#############################################################################
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
            return Response({"detail": "Invalid action. Use 'add' or 'remove'."}, status=400)

        if action == 'add':
            return Trip.add_member(trip, user_profile)
        elif action == 'remove':
            return Trip.remove_member(trip, user_profile)

    def validate_action(self, action):
        return action in ['add', 'remove']


#############################################################################
# Ticket
#############################################################################
@extend_schema(tags=['ticket'])
class TicketCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TicketCreateSerializer
    parser_classes = (MultiPartParser,)


@extend_schema(tags=['ticket'])
class TicketRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketRetrieveSerializer

    def get_object(self):
        id = self.kwargs['pk']
        return Ticket.objects.by_id(id)


@extend_schema(tags=['ticket'])
class TicketListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TicketListSerializer

    def get_queryset(self):
        user = self.request.user.get_default_profile()

        return Ticket.objects.by_user(user).select_related('profile', 'trip')


@extend_schema(tags=['ticket'])
class TicketUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketUpdateSerializer
    parser_classes = (MultiPartParser,)

    def get_object(self):
        id = self.kwargs['pk']
        return Ticket.objects.by_id(id)


@extend_schema(tags=['ticket'])
class TicketDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketDestroySerializer

    def get_object(self):
        id = self.kwargs['pk']
        return Ticket.objects.by_id(id)


#############################################################################
# Budget
#############################################################################
@extend_schema(tags=['budget'])
class BudgetUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetUpdateSerializer

    def get_object(self):
        trip = Trip.objects.by_id(self.kwargs['trip_id'])
        try:
            return trip.budżet
        except Budget.DoesNotExist:
            raise NotFound(detail="Nie znaleziono budżetu o podanym ID")


@extend_schema(tags=['budget'])
class BudgetDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetDestroySerializer

    def get_object(self):
        trip = Trip.objects.by_id(self.kwargs['trip_id'])
        try:
            return trip.budżet
        except Budget.DoesNotExist:
            raise NotFound(detail="Nie znaleziono budżetu o podanym ID")


#############################################################################
# Expense
#############################################################################
@extend_schema(tags=['expense'])
class ExpenseCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer


@extend_schema(tags=['expense'])
class ExpenseRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_object(self):
        try:
            return Expense.objects.get(pk=self.kwargs['pk'])
        except Expense.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wydatku o podanym ID")


@extend_schema(tags=['expense'])
class ExpenseListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(trip=self.kwargs['trip_id']).select_related('trip', 'user', 'category',
                                                                                  'currency')


@extend_schema(tags=['expense'])
class ExpenseUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_object(self):
        try:
            return Expense.objects.get(pk=self.kwargs['pk'])
        except Expense.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wydatku o podanym ID")


@extend_schema(tags=['expense'])
class ExpenseDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_object(self):
        try:
            return Expense.objects.get(pk=self.kwargs['pk'])
        except Expense.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wydatku o podanym ID")


#############################################################################
# Invitation
#############################################################################
@extend_schema(
    tags=['trip invitation'],
    request=InvitationSerializer,
    responses={200: OpenApiResponse(description="Zaproszenie wysłane!"), 400: OpenApiResponse(description="Niepoprawne dane zaproszenia.")}
)
class InviteUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, trip_id):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = data.get('user')
            is_guest = data.get('is_guest')

            if is_guest:
                user = CustomUser.create_guest_account(data['name'], data['email'])

            trip = Trip.objects.get(id=trip_id)
            invitation_link = self.create_invitation_link(request, trip, user)

            self.send_trip_invitation_email(data, invitation_link, trip)

            return Response({"message": "Zaproszenie wysłane!"}, status=status.HTTP_200_OK)

        return Response({"error": "Niepoprawne dane zaproszenia."}, status=status.HTTP_400_BAD_REQUEST)

    def create_invitation_link(self, request, trip, user):
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
        except TripAccessToken.DoesNotExist:
            raise Exception('Token nie został stworzony!')

    def send_trip_invitation_email(self, data, invitation_link, trip):
        subject = 'Zaproszenie do wycieczki Plannder'
        html_message = render_to_string('emails/trip_invitation_email.html', {
            'name': data['name'],
            'trip_name': trip.name,
            'date': data['date'],
            'trip_link': invitation_link
        })
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[data['email']],
            html_message=html_message,
        )


@extend_schema(
    tags=['trip invitation'],
)
class JoinTripAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[OpenApiParameter("token", str, description="Token dostępu do wycieczki", required=True)],
        responses={200: OpenApiResponse(description="Użytkownik dołączył do wycieczki!"),
                   400: OpenApiResponse(description="Brak tokenu w linku."),
                   404: OpenApiResponse(description="Podany token nie istnieje."),
                   403: OpenApiResponse(description="Konto użytkownika jest nieaktywne.")}
    )
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

        Trip.add_member(trip_access_token.trip, user_profile)
        login(request, user)

        return Response({"message": "Użytkownik dołączył do wycieczki!"})

    def get_trip_access_token(self, token):
        try:
            return TripAccessToken.objects.by_token(token)
        except TripAccessToken.DoesNotExist:
            return None
