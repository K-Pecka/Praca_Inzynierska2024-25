"""
Permission configuration for server project.
"""
from rest_framework.exceptions import NotFound
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
    Custom permission to check if the user is a participant of the trip.
    """
    message = "Tylko uczestnicy wycieczki mogą wykonać tę akcję."

    def has_permission(self, request, view):
        if isinstance(view, ListAPIView) or isinstance(view, CreateAPIView):
            return True

        try:
            obj = view.get_object()
        except Exception:
            return False

        profile = request.user.get_default_profile()
        if not profile:
            return False

        trip_related_objects = (
            Trip,
            Chatroom,
            ChatMessage,
            Ticket,
            Itinerary,
            ItineraryActivity,
        )

        for obj_type in trip_related_objects:
            if isinstance(obj, obj_type):
                return self.is_trip_participant(obj, profile)

        return False

    def is_trip_participant(self, obj, profile):
        if isinstance(obj, Trip):
            return obj.creator == profile or profile in obj.members.all()

        if isinstance(obj, Chatroom):
            return obj.trip.creator == profile or profile in obj.members.all()

        if isinstance(obj, ChatMessage):
            return obj.chatroom.trip.creator == profile or profile in obj.chatroom.members.all()

        if isinstance(obj, Ticket):
            return obj.trip.creator == profile or profile in obj.trip.members.all()

        if isinstance(obj, Itinerary):
            return obj.trip.creator == profile or profile in obj.trip.members.all()

        if isinstance(obj, ItineraryActivity):
            return obj.itinerary.trip.creator == profile or profile in obj.itinerary.trip.members.all()

        return False


class IsTripCreator(BasePermission):
    """
    Custom permission to check if the user is the creator of the trip.
    """
    message = "Tylko twórca wycieczki może wykonać tę akcję."

    def has_permission(self, request, view):
        profile = request.user.get_default_profile()
        if not profile:
            return False

        if request.method == 'POST':
            return self.is_creator_for_post_request(view, profile)

        try:
            obj = view.get_object()
        except Exception:
            return False

        return self.is_trip_creator(obj, profile)

    def is_creator_for_post_request(self, view, profile):
        """
        Handles POST requests to check if the user is the creator of the trip or itinerary.
        """
        trip = None
        trip_id = view.kwargs.get('trip_pk')

        if trip_id:
            trip = self.get_trip_by_id(trip_id)
        else:
            itinerary_id = view.kwargs.get('itinerary_pk')
            if itinerary_id:
                itinerary = self.get_itinerary_by_id(itinerary_id)
                trip = itinerary.trip if itinerary else None

        if not trip:
            return False

        return trip.creator == profile

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
