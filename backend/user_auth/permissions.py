from rest_framework.permissions import BasePermission


class IsGuideProfile(BasePermission):
    """
    Custom permission to check if the user is the creator for the chatroom.
    """
    message = 'Tylko przewodnik może wykonywać tę akcje.'

    def has_permission(self, request, view):
        profile = request.user.get_default_profile()

        if not profile:
            return False
        return profile.is_guide
