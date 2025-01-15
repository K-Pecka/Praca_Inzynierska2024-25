from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
)
from rest_framework.permissions import IsAuthenticated
from .models import Trip, TripActivity, Ticket
from .serializers import (
    TripSerializer, TripActivitySerializer, TicketSerializer
)


# Trip Views
class TripCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripSerializer


class TripRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripSerializer

    def get_object(self):
        return Trip.objects.get(pk=self.kwargs['pk'])


class TripUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripSerializer

    def get_object(self):
        return Trip.objects.get(pk=self.kwargs['pk'])


class TripDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripSerializer

    def get_object(self):
        return Trip.objects.get(pk=self.kwargs['pk'])


class TripListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripSerializer
    queryset = Trip.objects.all()


# TripActivity Views
class TripActivityCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripActivitySerializer


class TripActivityRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripActivitySerializer

    def get_object(self):
        return TripActivity.objects.get(pk=self.kwargs['pk'])


class TripActivityUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripActivitySerializer

    def get_object(self):
        return TripActivity.objects.get(pk=self.kwargs['pk'])


class TripActivityDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripActivitySerializer

    def get_object(self):
        return TripActivity.objects.get(pk=self.kwargs['pk'])


class TripActivityListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripActivitySerializer
    queryset = TripActivity.objects.all()


# Ticket Views
class TicketCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer


class TicketRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_object(self):
        return Ticket.objects.get(pk=self.kwargs['pk'])


class TicketUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_object(self):
        return Ticket.objects.get(pk=self.kwargs['pk'])


class TicketDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_object(self):
        return Ticket.objects.get(pk=self.kwargs['pk'])


class TicketListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
