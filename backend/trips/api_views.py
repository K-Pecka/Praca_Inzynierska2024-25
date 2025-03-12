from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
)
from rest_framework.permissions import IsAuthenticated

from .models import Trip, Ticket, Budget, Expense
from .serializers import (
    TripCreateSerializer, ExpenseSerializer,
    TicketCreateSerializer, TicketUpdateSerializer, TicketRetrieveSerializer, TicketDestroySerializer,
    TicketListSerializer, TripRetrieveSerializer, TripListSerializer, TripUpdateSerializer, TripDestroySerializer,
    BudgetUpdateSerializer, BudgetDestroySerializer, TripParticipantsListSerializer
)

from server.permissions import IsTripParticipant, IsTripCreator, IsTicketOwner


#############################################################################
# Trip
#############################################################################

@extend_schema(tags=['Trip'])
class TripCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripCreateSerializer


@extend_schema(tags=['Trip'])
class TripRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripRetrieveSerializer

    def get_object(self):
        id = self.kwargs['pk']
        return Trip.objects.by_id(id)


@extend_schema(tags=['Trip'])
class TripListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripListSerializer

    def get_queryset(self):
        user = self.request.user.get_default_profile()
        return Trip.objects.by_user(user).select_related('creator').prefetch_related('members')


@extend_schema(tags=['Trip'])
class TripUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripUpdateSerializer

    def get_object(self):
        id = self.kwargs['pk']
        return Trip.objects.by_id(id)


@extend_schema(tags=['Trip'])
class TripDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripDestroySerializer

    def get_object(self):
        id = self.kwargs['pk']
        return Trip.objects.by_id(id)


#############################################################################
# Participants
#############################################################################
@extend_schema(tags=['Trip'], parameters = [
    OpenApiParameter(name='email', description="Search users by email", required=False, type=str)
])
class TripParticipantsAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripParticipantsListSerializer

    def get_object(self):
        return Trip.objects.get(id=self.kwargs["pk"])

    def retrieve(self, request, *args, **kwargs):
        trip = self.get_object()

        search_query = self.request.query_params.get('email', None)

        if search_query:
            members = trip.members.filter(user__email__icontains=search_query)
        else:
            members = trip.members.all()

        print('members', members)

        serializer = self.get_serializer(members, many=True)

        return Response({"members": serializer.data})


#############################################################################
# Ticket
#############################################################################
@extend_schema(tags=['Ticket'])
class TicketCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TicketCreateSerializer
    parser_classes = (MultiPartParser,)


@extend_schema(tags=['Ticket'])
class TicketRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketRetrieveSerializer

    def get_object(self):
        id = self.kwargs['pk']
        return Ticket.objects.by_id(id)


@extend_schema(tags=['Ticket'])
class TicketListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TicketListSerializer

    def get_queryset(self):
        user = self.request.user.get_default_profile()

        return Ticket.objects.by_user(user).select_related('profile', 'trip')


@extend_schema(tags=['Ticket'])
class TicketUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketUpdateSerializer
    parser_classes = (MultiPartParser,)

    def get_object(self):
        id = self.kwargs['pk']
        return Ticket.objects.by_id(id)


@extend_schema(tags=['Ticket'])
class TicketDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketDestroySerializer

    def get_object(self):
        id = self.kwargs['pk']
        return Ticket.objects.by_id(id)


#############################################################################
# Budget
#############################################################################
@extend_schema(tags=['Budget'])
class BudgetUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetUpdateSerializer

    def get_object(self):
        trip = Trip.objects.by_id(self.kwargs['trip_id'])
        try:
            return trip.budżet
        except Budget.DoesNotExist:
            raise NotFound(detail="Nie znaleziono budżetu o podanym ID")


@extend_schema(tags=['Budget'])
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
@extend_schema(tags=['Expense'])
class ExpenseCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer


@extend_schema(tags=['Expense'])
class ExpenseRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_object(self):
        try:
            return Expense.objects.get(pk=self.kwargs['pk'])
        except Expense.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wydatku o podanym ID")


@extend_schema(tags=['Expense'])
class ExpenseListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(trip=self.kwargs['trip_id']).select_related('trip', 'user')


@extend_schema(tags=['Expense'])
class ExpenseUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_object(self):
        try:
            return Expense.objects.get(pk=self.kwargs['pk'])
        except Expense.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wydatku o podanym ID")


@extend_schema(tags=['Expense'])
class ExpenseDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_object(self):
        try:
            return Expense.objects.get(pk=self.kwargs['pk'])
        except Expense.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wydatku o podanym ID")
