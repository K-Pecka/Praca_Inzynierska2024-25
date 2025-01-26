from rest_framework.permissions import BasePermission

from trips.models import Trip, TripActivity, Ticket


class IsTripParticipant(BasePermission):
    """
    Custom permission to check if the user is the creator for the chatroom.
    """
    message = "Tylko uczestnicy wycieczki mogą wykonać tę akcje."

    def has_permission(self, request, view):
        obj = view.get_object()
        profile = request.user.get_default_profile()
        if isinstance(obj, Trip):
            return obj.creator == profile or profile in obj.members.all()
        elif isinstance(obj, TripActivity) or isinstance(obj, Ticket):
            return obj.trip.creator == profile or profile in obj.trip.members.all()
        return False


class IsTripCreator(BasePermission):
    """
    Custom permission to check if the user is the creator for the chatroom.
    """
    message = "Tylko stwórca wycieczki może wykonać tę akcje."

    def has_permission(self, request, view):
        obj = view.get_object()
        profile = request.user.get_default_profile()
        if isinstance(obj, Trip):
            return obj.creator == profile
        if isinstance(obj, TripActivity) or isinstance(obj, Ticket):
            return obj.trip.creator == profile
        return False


class IsTicketOwner(BasePermission):
    """
    Custom permission to check if the user is the creator for the ticket.
    """
    message = "Tylko stwórca biletu może wykonać tę akcje."

    def has_permission(self, request, view):
        obj = view.get_object()
        profile = request.user.get_default_profile()
        if isinstance(obj, Ticket):
            return obj.profile == profile
        return False

