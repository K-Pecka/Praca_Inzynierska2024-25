from rest_framework.permissions import BasePermission
from chats.models import Chatroom, ChatMessage
from trips.models import Trip, TripActivity, Ticket


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
    message = "Tylko uczestnicy czatu mogą wykonać tę akcje."

    def has_permission(self, request, view):
        obj = None
        if hasattr(view, 'get_object'):
            try:
                obj = view.get_object()
            except Exception:
                pass

        if not obj:
            chatroom_id = view.request.data.get('chatroom')
            if chatroom_id:
                obj = Chatroom.objects.filter(pk=chatroom_id).first()

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
    Custom permission to check if the user is the creator for the chatroom.
    """
    message = "Tylko uczestnicy wycieczki mogą wykonać tę akcje."

    def has_permission(self, request, view):
        obj = view.get_object()
        profile = request.user.get_default_profile()

        if isinstance(obj, Trip):
            return obj.creator == profile or profile in obj.members.all()
        if isinstance(obj, TripActivity) or isinstance(obj, Ticket):
            return obj.trip.creator == profile or profile in obj.trip.members.all()
        if isinstance(obj, Chatroom):
            return obj.trip.creator == profile or profile in obj.members.all()
        if isinstance(obj, ChatMessage):
            return obj.chatroom.trip.creator == profile or profile in obj.chatroom.members.all()
        if isinstance(obj, Ticket):
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
        if isinstance(obj, Chatroom):
            return obj.trip.creator == profile
        if isinstance(obj, ChatMessage):
            return obj.chatroom.trip.creator == profile
        if isinstance(obj, Ticket):
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
