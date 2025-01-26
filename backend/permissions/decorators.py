from functools import wraps

from django.http import HttpResponseForbidden
from rest_framework.exceptions import PermissionDenied

from users.models import UserProfile


def required_permission(permission_code, action):
    """
    Decorator to check if the user has the specified permission.
    Usage:
        @check_perms('app_label.permission_codename')
        def my_view(request):
            ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            profile = request.user.get_default_profile()

            if profile is None:
                raise PermissionDenied

            permission = profile.profile_to_permission.filter(permission__code=permission_code).first()

            if permission is None:
                return HttpResponseForbidden("You do not have permission to perform this action.")

            has_permission = getattr(permission, f'can_{action.lower()}', None)

            if not has_permission:
                return HttpResponseForbidden("You do not have permission to perform this action.")

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator
