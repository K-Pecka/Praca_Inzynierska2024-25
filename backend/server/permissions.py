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
        obj = view.get_object()
        if isinstance(obj, Chatroom):
            profile = request.user.get_default_profile()
            return obj.creator == profile
        return False


class IsParticipantForChatroom(BasePermission):
    """
    Custom permission to check if the user is the creator for the chatroom.
    """
    message = "Tylko uczestnicy czatu mogą wykonać tę akcję."

    def has_permission(self, request, view):
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

        if not obj:
            return False

        profile = request.user.get_default_profile()

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
        obj = view.get_object()
        if isinstance(obj, ChatMessage):
            profile = request.user.get_default_profile()
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
        if isinstance(view, ListAPIView):
            return True  # No need for object checking in ListAPIView

        # Don't call get_object for CreateAPIView (which doesn't require it)
        if isinstance(view, CreateAPIView):
            return True

        try:
            obj = view.get_object()  # Only for views that require fetching objects
            print('obj', obj)
        except Exception:
            print('ex', view.get_object())
            return False

        profile = request.user.get_default_profile()
        if not profile:
            print('no profile')
            return False

        if isinstance(obj, Trip):
            print(f'obj.creator: {obj.creator}, profile: {profile}, obj.members: {obj.members.all()}')
            print('res', obj.creator == profile or profile in obj.members.all())
            return obj.creator == profile or profile in obj.members.all()

        if isinstance(obj, Chatroom):
            print(f'obj.creator: {obj.trip.creator}, profile: {profile}, obj.members: {obj.members.all()}')
            print('res', obj.trip.creator == profile or profile in obj.members.all())
            return obj.trip.creator == profile or profile in obj.members.all()

        if isinstance(obj, ChatMessage):
            print(f'obj.creator: {obj.chatroom.trip.creator}, profile: {profile}, obj.members: {obj.chatroom.members.all()}')
            print('res', obj.chatroom.trip.creator == profile or profile in obj.chatroom.members.all())
            return obj.chatroom.trip.creator == profile or profile in obj.chatroom.members.all()

        if isinstance(obj, Ticket):
            print(f'obj.creator: {obj.trip.creator}, profile: {profile}, obj.members: {obj.trip.members.all()}')
            print('res', obj.trip.creator == profile or profile in obj.trip.members.all())
            return obj.trip.creator == profile or profile in obj.trip.members.all()

        if isinstance(obj, Itinerary):
            print(f'obj.creator: {obj.trip.creator}, profile: {profile}, obj.members: {obj.trip.members.all()}')
            print('res', obj.trip.creator == profile or profile in obj.trip.members.all())
            return obj.trip.creator == profile or profile in obj.trip.members.all()

        if isinstance(obj, ItineraryActivity):
            print(f'obj.creator: {obj.itinerary.trip.creator}, profile: {profile}, obj.members: {obj.itinerary.trip.members.all()}')
            print('res', obj.itinerary.trip.creator == profile or profile in obj.itinerary.trip.members.all())
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
            trip_id = view.kwargs.get('trip_pk')
            if trip_id:
                try:
                    trip = Trip.objects.get(pk=trip_id)
                except Trip.DoesNotExist:
                    raise NotFound(detail="Wycieczka o podanym ID nie istnieje.")
            else:
                itinerary_id = view.kwargs.get('itinerary_pk')
                if not itinerary_id:
                    return False
                try:
                    itinerary = Itinerary.objects.get(pk=itinerary_id)
                except Itinerary.DoesNotExist:
                    raise NotFound(detail="Plan wycieczki o podanym ID nie istnieje.")
                trip = itinerary.trip
            return trip.creator == profile
        else:
            try:
                obj = view.get_object()
            except Exception:
                return False

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
        obj = view.get_object()
        profile = request.user.get_default_profile()
        if isinstance(obj, Ticket):
            return obj.profile == profile
        return False
