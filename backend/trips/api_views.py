from django.db.models import Q
from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, get_object_or_404
)
from rest_framework.permissions import IsAuthenticated

from .models import Trip, TripActivity, Ticket
from .permissions import IsTripParticipant, IsTripCreator, IsTicketOwner
from .serializers import (
    TripSerializer, TripActivitySerializer, TicketSerializer, TripCreateSerializer
)


# Trip Views
class TripCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripCreateSerializer


class TripRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripSerializer

    def get_object(self):
        try:
            return Trip.objects.get(pk=self.kwargs['pk'])
        except Trip.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wycieczki o podanym ID")


class TripListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripSerializer

    def get_queryset(self):
        profile = self.request.user_profile
        return Trip.objects.filter(
            Q(creator=profile) | Q(members=profile)
        ).distinct().select_related('creator').prefetch_related('members')


class TripUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripSerializer

    def get_object(self):
        try:
            return Trip.objects.get(pk=self.kwargs['pk'])
        except Trip.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wycieczki o podanym ID")


class TripDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripSerializer

    def get_object(self):
        try:
            return Trip.objects.get(pk=self.kwargs['pk'])
        except Trip.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wycieczki o podanym ID")


# TripActivity Views
class TripActivityCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripActivitySerializer


class TripActivityRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripActivitySerializer

    def get_object(self):
        try:
            return TripActivity.objects.get(trip=self.kwargs['trip_id'], pk=self.kwargs['pk'])
        except TripActivity.DoesNotExist:
            raise NotFound(detail="Nie znaleziono aktywności wycieczki o podanym ID")


class TripActivityListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripActivitySerializer

    def get_queryset(self):
        return TripActivity.objects.filter(trip=self.kwargs['trip_id']).select_related('trip')


class TripActivityUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripActivitySerializer

    def get_object(self):
        try:
            return TripActivity.objects.get(trip=self.kwargs['trip_id'], pk=self.kwargs['pk'])
        except TripActivity.DoesNotExist:
            raise NotFound(detail="Nie znaleziono aktywności wycieczki o podanym ID")


class TripActivityDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripActivitySerializer

    def get_object(self):
        try:
            return TripActivity.objects.get(trip=self.kwargs['trip_id'], pk=self.kwargs['pk'])
        except TripActivity.DoesNotExist:
            raise NotFound(detail="Nie znaleziono aktywności wycieczki o podanym ID")


# Ticket Views
class TicketCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TicketSerializer


class TicketRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTicketOwner]
    serializer_class = TicketSerializer

    def get_object(self):
        try:
            return Ticket.objects.get(pk=self.kwargs['pk'])
        except Ticket.DoesNotExist:
            raise NotFound(detail="Nie znaleziono biletu o podanym ID")


class TicketListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(profile=self.request.user_profile)


class TicketUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTicketOwner]
    serializer_class = TicketSerializer

    def get_object(self):
        try:
            return Ticket.objects.get(pk=self.kwargs['pk'])
        except Ticket.DoesNotExist:
            raise NotFound(detail="Nie znaleziono biletu o podanym ID")


class TicketDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTicketOwner]
    serializer_class = TicketSerializer

    def get_object(self):
        try:
            return Ticket.objects.get(pk=self.kwargs['pk'])
        except Ticket.DoesNotExist:
            raise NotFound(detail="Nie znaleziono biletu o podanym ID")
