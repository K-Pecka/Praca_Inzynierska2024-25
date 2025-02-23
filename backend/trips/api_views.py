from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
)
from rest_framework.permissions import IsAuthenticated

from .models import Trip, Ticket, Budget, Expense
from server.permissions import IsTripParticipant, IsTripCreator, IsTicketOwner
from .serializers import (
    TripSerializer, TicketSerializer, TripCreateSerializer, BudgetSerializer, ExpenseSerializer, BudgetCreateSerializer
)


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
    serializer_class = TripSerializer

    def get_object(self):
        return Trip.objects.by_id(self.kwargs['pk'])


@extend_schema(tags=['Trip'])
class TripListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripSerializer

    def get_queryset(self):
        profile = self.request.user.get_default_profile()

        return Trip.objects.by_user(profile).select_related('creator').prefetch_related('members')


@extend_schema(tags=['Trip'])
class TripUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripSerializer

    def get_object(self):
        return Trip.objects.by_id(self.kwargs['pk'])


@extend_schema(tags=['Trip'])
class TripDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripSerializer

    def get_object(self):
        return Trip.objects.by_id(self.kwargs['pk'])


#############################################################################
# Ticket
#############################################################################
@extend_schema(tags=['Ticket'])
class TicketCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripCreateSerializer


@extend_schema(tags=['Ticket'])
class TicketRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketSerializer

    def get_object(self):
        return Ticket.objects.by_id(self.kwargs['pk']).select_related('profile', 'trip', 'activity')


@extend_schema(tags=['Ticket'])
class TicketListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TicketSerializer

    def get_queryset(self):
        profile = self.request.user.get_default_profile()

        return Ticket.objects.by_user(profile).select_related('profile', 'trip', 'activity')


@extend_schema(tags=['Ticket'])
class TicketUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketSerializer

    def get_object(self):
        return Ticket.objects.by_id(self.kwargs['pk']).select_related('profile', 'trip', 'activity')


@extend_schema(tags=['Ticket'])
class TicketDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketSerializer

    def get_object(self):
        return Ticket.objects.by_id(self.kwargs['pk']).select_related('profile', 'trip', 'activity')


#############################################################################
# Budget
#############################################################################
@extend_schema(tags=['Budget'])
class BudgetCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetCreateSerializer


@extend_schema(tags=['Budget'])
class BudgetUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer

    def get_object(self):
        trip = Trip.objects.by_id(self.kwargs['trip_id'])
        try:
            return trip.budżet
        except Budget.DoesNotExist:
            raise NotFound(detail="Nie znaleziono budżetu o podanym ID")


@extend_schema(tags=['Budget'])
class BudgetDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer

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
