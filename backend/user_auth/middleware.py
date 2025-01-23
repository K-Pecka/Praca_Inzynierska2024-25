from django.shortcuts import get_object_or_404
from users.models import UserProfile


class AttachProfileMiddleware:
    """
    Middleware to attach the user's profile to the request object
    after successful authentication.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                profile = get_object_or_404(UserProfile, user=request.user.id, is_default=True)
                request.user_profile = profile
            except UserProfile.DoesNotExist:
                request.user_profile = None

        response = self.get_response(request)
        return response
