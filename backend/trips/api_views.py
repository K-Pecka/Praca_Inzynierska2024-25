from django.db.models import Q
from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
)
from rest_framework.permissions import IsAuthenticated

from .models import Trip, Ticket, Budget, Expense
from server.permissions import IsTripParticipant, IsTripCreator, IsTicketOwner
from .serializers import (
    TripSerializer, TicketSerializer, TripCreateSerializer, BudgetSerializer, ExpenseSerializer
)


#############################################################################
# Trip
#############################################################################
class TripCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripCreateSerializer


class TripRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripSerializer

    def get_object(self):
        return Trip.objects.by_id(self.kwargs['pk'])


class TripListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripSerializer

    def get_queryset(self):
        profile = self.request.user.get_default_profile()

        return Trip.objects.by_user(profile).select_related('creator').prefetch_related('members')


class TripUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripSerializer

    def get_object(self):
        return Trip.objects.by_id(self.kwargs['pk'])


class TripDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripSerializer

    def get_object(self):
        return Trip.objects.by_id(self.kwargs['pk'])


#############################################################################
# Ticket
#############################################################################
class TicketCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TicketSerializer


class TicketRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketSerializer

    def get_object(self):
        return Ticket.objects.by_id(self.kwargs['pk']).select_related('profile', 'trip', 'activity')


class TicketListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TicketSerializer

    def get_queryset(self):
        profile = self.request.user.get_default_profile()

        return Ticket.objects.by_user(profile).select_related('profile', 'trip', 'activity')


class TicketUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketSerializer

    def get_object(self):
        return Ticket.objects.by_id(self.kwargs['pk']).select_related('profile', 'trip', 'activity')


class TicketDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketSerializer

    def get_object(self):
        return Ticket.objects.by_id(self.kwargs['pk']).select_related('profile', 'trip', 'activity')


class BudgetCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer


class BudgetRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer

    def get_object(self):
        try:
            return Budget.objects.get(pk=self.kwargs['pk'])
        except Budget.DoesNotExist:
            raise NotFound(detail="Nie znaleziono budżetu o podanym ID")


class BudgetUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer

    def get_object(self):
        try:
            return Budget.objects.get(pk=self.kwargs['pk'])
        except Budget.DoesNotExist:
            raise NotFound(detail="Nie znaleziono budżetu o podanym ID")


class BudgetDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer

    def get_object(self):
        try:
            return Budget.objects.get(pk=self.kwargs['pk'])
        except Budget.DoesNotExist:
            raise NotFound(detail="Nie znaleziono budżetu o podanym ID")


class ExpenseCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer


class ExpenseRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_object(self):
        try:
            return Expense.objects.get(pk=self.kwargs['pk'])
        except Expense.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wydatku o podanym ID")


class ExpenseListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(trip=self.kwargs['trip_id']).select_related('trip', 'user')


class ExpenseUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_object(self):
        try:
            return Expense.objects.get(pk=self.kwargs['pk'])
        except Expense.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wydatku o podanym ID")


class ExpenseDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_object(self):
        try:
            return Expense.objects.get(pk=self.kwargs['pk'])
        except Expense.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wydatku o podanym ID")
