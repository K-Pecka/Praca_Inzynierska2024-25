"""
Permission configuration for server project.
"""
from django.core.exceptions import ValidationError

from rest_framework.exceptions import NotFound, PermissionDenied, AuthenticationFailed
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import BasePermission

from chats.models import Chatroom, Message
from trips.models import Trip, Ticket, Expense, TripAccessToken, DetailedExpense
from itineraries.models import Itinerary, ItineraryActivity

##################################################################################
# Chat permissions
##################################################################################
class IsCreatorForChatroom(BasePermission):
    """
    Custom permission to check if the user is the creator for the chatroom.
    """
    message = 'Tylko właściel czatu może wykonywać tę akcje.'

    def has_permission(self, request, view):
        try:
            obj = view.get_object()
        except Exception:
            return False

        if isinstance(obj, Chatroom):
            profile = request.user.get_default_profile()
            if not profile:
                return False
            return obj.creator == profile

        return False


class IsParticipantForChatroom(BasePermission):
    """
    Custom permission to check if the user is the creator for the chatroom.
    """
    message = "Tylko uczestnicy czatu mogą wykonać tę akcję."

    def has_permission(self, request, view):
        obj = self.get_object_from_view_or_request(request, view)

        if not obj:
            return False

        profile = request.user.get_default_profile()
        if not profile:
            return False

        trip_related_objects = (Chatroom, Message)

        for obj_type in trip_related_objects:
            if isinstance(obj, obj_type):
                return self.is_participant_for_chatroom(obj, profile)

        return False

    def get_object_from_view_or_request(self, request, view):
        """
        Helper function to get the object either from the view or request data.
        """
        obj = None

        if hasattr(view, 'get_object') and not isinstance(view, ListAPIView):
            try:
                obj = view.get_object()
            except AssertionError:
                obj = None

        if not obj:
            chatroom_id = request.data.get('chatroom') or view.kwargs.get('room_pk')
            if chatroom_id:
                obj = Chatroom.objects.filter(pk=chatroom_id).first()

        return obj

    def is_participant_for_chatroom(self, obj, profile):
        if isinstance(obj, Chatroom):
            return obj.creator == profile or profile in obj.members.all()

        elif isinstance(obj, Message):
            return obj.chatroom.creator == profile or profile in obj.chatroom.members.all()
        return False


class IsCreatorForMessage(BasePermission):
    """
    Custom permission to check if the user is the creator for the chat message.
    """
    message = 'Tylko właściel wiadomości może wykonywać tę akcje.'

    def has_permission(self, request, view):
        try:
            obj = view.get_object()
        except Exception:
            return False

        if isinstance(obj, Message):
            profile = request.user.get_default_profile()
            if not profile:
                return False
            return obj.profile == profile

        return False


##################################################################################3
# Trip permissions
##################################################################################3
class IsTripParticipant(BasePermission):
    """
    Custom permission that:
    - Allows all actions for list/create views
    - Returns 404 when object doesn't exist
    - Returns 403 only when object exists but user has no permissions
    """
    message = "Tylko uczestnicy wycieczki mogą wykonać tę akcję."

    def has_permission(self, request, view):
        if isinstance(view, (ListAPIView, CreateAPIView)) or hasattr(view, 'action') and view.action in ['list', 'create']:
            return True

        try:
            obj = view.get_object()
        except NotFound:
            raise
        except Exception:
            raise NotFound("Nie znaleziono obiektu")

        profile = request.user.get_default_profile()
        if not profile:
            raise PermissionDenied("Nie znaleziono profilu użytkownika")

        if not self.is_trip_participant(obj, profile):
            raise PermissionDenied(self.message)

        return True

    def is_trip_participant(self, obj, profile):
        """Check if profile is a participant of related trip"""
        trip = self.get_related_trip(obj)
        if not trip:
            return False
        if trip.creator.pk == profile.pk or trip.members.filter(pk=profile.pk).exists():
            return True
        return None

    def get_related_trip(self, obj):
        """
        Get the related trip based on object type
        """
        if isinstance(obj, Trip):
            return obj
        elif isinstance(obj, Chatroom):
            return obj.trip
        elif isinstance(obj, Message):
            return obj.chatroom.trip
        elif isinstance(obj, Ticket):
            return obj.trip
        elif isinstance(obj, Itinerary):
            return obj.trip
        elif isinstance(obj, ItineraryActivity):
            return obj.itinerary.trip
        elif isinstance(obj, Expense):
            return obj.trip
        elif isinstance(obj, DetailedExpense):
            return obj.trip
        return None


class IsTripCreator(BasePermission):
    """
    Custom permission to check if the user is the creator of the trip.
    """
    message = "Tylko twórca wycieczki może wykonać tę akcję."

    def has_permission(self, request, view):
        profile = request.user.get_default_profile()
        if not profile:
            return False

        if request.method == 'POST' or request.method == 'DELETE':
            return self.is_creator_for_post_request(view, profile)

        try:
            obj = view.get_object()
            return self.is_trip_creator(obj, profile)
        except NotFound:
            raise
        except Exception:
            return False

    def is_creator_for_post_request(self, view, profile):
        """
        Handles POST requests to check if the user is the creator of the trip or itinerary.
        """
        trip = None
        trip_pk = view.kwargs.get('trip_pk')
        itinerary_id = view.kwargs.get('itinerary_pk')

        obj = None
        if not trip_pk and not itinerary_id and hasattr(view, 'get_object'):
            try:
                obj = view.get_object()
            except Exception:
                pass

        if not trip_pk and isinstance(obj, Trip):
            trip_pk = obj.pk

        if not itinerary_id and isinstance(obj, Itinerary):
            itinerary_id = obj.pk

        if trip_pk:
            trip = Trip.objects.filter(pk=trip_pk).first()
        elif itinerary_id:
            itinerary = Itinerary.objects.filter(pk=itinerary_id).first()
            if itinerary:
                trip = itinerary.trip

        if not trip:
            raise NotFound(detail="Nie znaleziono wycieczki.")

        if trip.creator != profile:
            raise PermissionDenied(self.message)

        return True

    def is_trip_creator(self, obj, profile):
        if isinstance(obj, Trip):
            return obj.creator == profile
        if isinstance(obj, Chatroom):
            return obj.trip.creator == profile
        if isinstance(obj, Message):
            return obj.chatroom.trip.creator == profile
        if isinstance(obj, Ticket):
            return obj.trip.creator == profile
        if isinstance(obj, Itinerary):
            return obj.trip.creator == profile
        if isinstance(obj, ItineraryActivity):
            return obj.itinerary.trip.creator == profile
        if isinstance(obj, Expense):
            return obj.trip.creator == profile
        if isinstance(obj, DetailedExpense):
            return obj.trip.creator == profile
        return False


class IsTicketOwner(BasePermission):
    """
    Custom permission to check if the user is the creator or shared profile for the ticket.
    """
    message = "Tylko właściciel lub współdzielony profil ma dostęp do tego biletu."

    def has_object_permission(self, request, view, obj):
        profile = request.user.get_default_profile()
        if not profile:
            return False
        return obj.owner == profile or profile in obj.profiles.all()


class IsExpenseOwnerOrTripCreator(BasePermission):
    """
    Permission class to check if the user is the owner of an expense.

    This permission ensures that only the owner of a specific expense has the
    rights to access or modify it. It performs a validation by cross-checking
    the user associated with the request against the owner of the expense
    instance being accessed.

    Attributes:
        None
    """
    message = "Tylko właściciel wydatku lub przewodnik wycieczki może wykonać tę akcję."

    def has_object_permission(self, request, view, obj):
        return request.user.get_default_profile() in [obj.user, obj.trip.creator]


class IsAuthenticatedOrValidTripToken(BasePermission):
    """
    Pozwala użytkownikowi jeśli jest zalogowany
    LUB posiada poprawny token do wycieczki w URL-u (?trip_token=...)
    """

    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')

        if auth_header:
            parts = auth_header.split()
            if not parts:
                raise ValidationError('Niepoprawny format tokenu.')

            if len(parts) != 2 or parts[0].lower() != 'bearer':
                raise AuthenticationFailed('Niepoprawny format tokenu.')

            token = parts[1]
            trip_token = TripAccessToken.objects.filter(token=token).first()
            if trip_token:
                return True

        user = getattr(request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            return True
        return False


class IsTripCreatorOrTargetUser(BasePermission):
    """
    Custom permission to check if the user is either the trip creator or an allowed target user (e.g., participant).
    """
    message = "Tylko twórca wycieczki lub uprawniony uczestnik może wykonać tę akcję."

    def has_permission(self, request, view):
        profile = request.user.get_default_profile()
        if not profile:
            return False

        return self.is_creator_or_participant_for_post(view, profile)

    def has_object_permission(self, request, view, obj):
        profile = request.user.get_default_profile()
        if not profile:
            return False
        return self.is_trip_creator_or_target(obj, profile)

    def is_creator_or_participant_for_post(self, view, profile):
        """
        Checks if the user is the creator or a participant in the trip or related itinerary.
        """
        trip = self.get_trip_from_view(view)
        if not trip:
            raise NotFound(detail="Nie znaleziono wycieczki.")

        request = getattr(self, 'request', None)
        target_profile = profile
        user_profile = request.user.get_default_profile()

        if target_profile == user_profile:
            return True

        if trip.creator == profile or profile in trip.members.all():
            return True

        raise PermissionDenied(self.message)

    def is_trip_creator_or_target(self, obj, profile):
        """
        Checks if the user is the trip creator or the target user (e.g., involved participant).
        """
        trip = self.extract_trip_from_obj(obj)

        request = getattr(self, 'request', None)
        target_profile = profile
        user_profile = request.user.get_default_profile()

        if target_profile == user_profile:
            return True

        if not trip:
            return False

        return trip.creator == profile or profile in trip.participants.all()

    def get_trip_from_view(self, view):
        """
        Retrieves the Trip object from the view kwargs or associated object.
        """
        trip_pk = view.kwargs.get('trip_pk')
        itinerary_pk = view.kwargs.get('itinerary_pk')
        obj = None

        if not trip_pk and not itinerary_pk and hasattr(view, 'get_object'):
            try:
                obj = view.get_object()
            except Exception:
                pass

        if isinstance(obj, Trip):
            return obj
        elif isinstance(obj, Itinerary):
            return obj.trip

        if trip_pk:
            return Trip.objects.filter(pk=trip_pk).first()
        if itinerary_pk:
            itinerary = Itinerary.objects.filter(pk=itinerary_pk).first()
            return itinerary.trip if itinerary else None

        return None

    def extract_trip_from_obj(self, obj):
        """
        Retrieves the Trip object related to various models.
        """
        if isinstance(obj, Trip):
            return obj
        elif isinstance(obj, Chatroom):
            return obj.trip
        elif isinstance(obj, Message):
            return obj.chatroom.trip
        elif isinstance(obj, Ticket):
            return obj.trip
        elif isinstance(obj, Itinerary):
            return obj.trip
        elif isinstance(obj, ItineraryActivity):
            return obj.itinerary.trip
        elif isinstance(obj, Expense):
            return obj.trip
        elif isinstance(obj, DetailedExpense):
            return obj.trip
        return False
