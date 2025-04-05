"""
Permission configuration for server project.
"""
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import BasePermission
from chats.models import Chatroom, ChatMessage
from trips.models import Trip, Ticket
from itineraries.models import Itinerary, ItineraryActivity


##################################################################################3
# Chat permissions
##################################################################################3
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

        trip_related_objects = (Chatroom, ChatMessage)

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

        elif isinstance(obj, ChatMessage):
            return obj.chatroom.creator == profile or profile in obj.chatroom.members.all()
        return False


class IsCreatorForChatMessage(BasePermission):
    """
    Custom permission to check if the user is the creator for the chat message.
    """
    message = 'Tylko właściel wiadomości może wykonywać tę akcje.'

    def has_permission(self, request, view):
        try:
            obj = view.get_object()
        except Exception:
            return False

        if isinstance(obj, ChatMessage):
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
        if isinstance(view, (ListAPIView, CreateAPIView)):
            return True

        try:
            obj = view.get_object()
        except NotFound:
            raise
        except Exception as e:
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
        return trip.creator == profile or profile in trip.members.all()

    def get_related_trip(self, obj):
        """
        Get the related trip based on object type
        """
        if isinstance(obj, Trip):
            return obj
        elif isinstance(obj, Chatroom):
            return obj.trip
        elif isinstance(obj, ChatMessage):
            return obj.chatroom.trip
        elif isinstance(obj, Ticket):
            return obj.trip
        elif isinstance(obj, Itinerary):
            return obj.trip
        elif isinstance(obj, ItineraryActivity):
            return obj.itinerary.trip
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
        trip_id = view.kwargs.get('trip_pk')
        itinerary_id = view.kwargs.get('itinerary_pk')

        obj = None
        if not trip_id and not itinerary_id and hasattr(view, 'get_object'):
            try:
                obj = view.get_object()
            except Exception:
                pass

        if not trip_id and isinstance(obj, Trip):
            trip_id = obj.pk

        if not itinerary_id and isinstance(obj, Itinerary):
            itinerary_id = obj.pk

        if trip_id:
<<<<<<< HEAD
            trip = Trip.objects.get(pk=trip_id)
        else:
            itinerary_id = view.kwargs.get('itinerary_pk')
            if itinerary_id:
                itinerary = Itinerary.objects.get(pk=itinerary_id)
                trip = itinerary.trip if itinerary else None
        if trip is None:
            raise NotFound(detail="Nie znaleziono wycieczki.")

        if trip.creator != profile:
            raise PermissionDenied(self.message)

=======
            trip = Trip.objects.filter(pk=trip_id).first()
        elif itinerary_id:
            itinerary = Itinerary.objects.filter(pk=itinerary_id).first()
            if itinerary:
                trip = itinerary.trip

        if not trip:
            raise NotFound(detail="Nie znaleziono wycieczki.")

        if trip.creator != profile:
            raise PermissionDenied(self.message)

>>>>>>> 8f4151a (Update version 0.1)
        return True

    def is_trip_creator(self, obj, profile):
        if isinstance(obj, Trip):
            return obj.creator == profile
        if isinstance(obj, Chatroom):
            return obj.trip.creator == profile
        if isinstance(obj, ChatMessage):
            return obj.chatroom.trip.creator == profile
        if isinstance(obj, Ticket):
            return obj.trip.creator == profile
        if isinstance(obj, Itinerary):
            return obj.trip.creator == profile
        if isinstance(obj, ItineraryActivity):
            return obj.itinerary.trip.creator == profile
        return False


class IsTicketOwner(BasePermission):
    """
    Custom permission to check if the user is the creator for the ticket.
    """
    message = "Tylko stwórca biletu może wykonać tę akcje."

    def has_permission(self, request, view):
        try:
            obj = view.get_object()
        except Ticket.DoesNotExist:
            raise NotFound(detail="Bilet o podanym ID nie istnieje.")
        except Exception:
            return False

        profile = request.user.get_default_profile()
        if not profile:
            return False

        if isinstance(obj, Ticket):
            return obj.profile == profile

        return False
