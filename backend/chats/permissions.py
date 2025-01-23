from rest_framework.permissions import BasePermission
from .models import Chatroom, UserProfile, ChatMessage


class IsCreatorForChatroom(BasePermission):
    """
    Custom permission to check if the user is the creator for the chatroom.
    """
    message = 'Tylko właściel czatu może wykonywać tę akcje.'

    def has_permission(self, request, view):
        obj = view.get_object()
        if isinstance(obj, Chatroom):
            profile = getattr(request, 'user_profile', None)
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

        profile = getattr(request, 'user_profile', None)

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
            profile = getattr(request, 'user_profile', None)
            return obj.profile == profile
        return False
