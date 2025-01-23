from rest_framework.permissions import BasePermission
from .models import Chatroom, UserProfile, ChatMessage


class IsOwnerForChatroom(BasePermission):
    """
    Custom permission to check if the user is the guide for the chatroom.
    """
    message = 'Tylko właściel czatu może wykonywać tę akcje.'

    def has_permission(self, request, view):
        obj = view.get_object()
        if isinstance(obj, Chatroom):
            profile = getattr(request, 'user_profile', None)
            return obj.owner == profile
        return False


class IsParticipantForChatroom(BasePermission):
    """
    Custom permission to check if the user is the guide for the chatroom.
    """
    message = "Tylko uczestnicy czatu mogą wykonać tę akcje."

    def has_permission(self, request, view):
        obj = view.get_object()
        if isinstance(obj, Chatroom):
            profile = getattr(request, 'user_profile', None)
            return obj.owner == profile or profile in obj.tourists.all()
        return False


class CanSendMessageInChatroom(BasePermission):
    """
    Custom permission to check if the user is the guide for the chatroom.
    """
    message = "Tylko uczestnicy czatu mogą wykonać tę akcje."

    def has_permission(self, request, view):
        chatroom_id = request.data.get('chatroom') or view.kwargs.get('chatroom_id')

        if not chatroom_id:
            return False

        try:
            chatroom = Chatroom.objects.get(id=chatroom_id)
        except Chatroom.DoesNotExist:
            return False

        profile = getattr(request, 'user_profile', None)
        if not profile:
            return False

        return chatroom.owner == profile or profile in chatroom.tourists.all()


class IsOwnerForChatMessage(BasePermission):
    """
    Custom permission to check if the user is the owner for the chat message.
    """
    message = 'Tylko właściel wiadomości może wykonywać tę akcje.'

    def has_permission(self, request, view):
        obj = view.get_object()
        if isinstance(obj, ChatMessage):
            profile = getattr(request, 'user_profile', None)
            return obj.profile == profile
        return False
