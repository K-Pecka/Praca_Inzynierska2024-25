from functools import wraps

from django.http import HttpResponseForbidden
from rest_framework.exceptions import PermissionDenied


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
        def _wrapped_view(view, request, *args, **kwargs):
            profile = getattr(request.profile, 'guideprofile', None)

            if profile is None:
                raise PermissionDenied

            permission = request.profile.profile_to_permission.filter(permission__code=permission_code).first().permission

            if permission is None:
                return HttpResponseForbidden("You do not have permission to perform this action.")

            actions_mapping = {
                'READ': permission.can_view,
                'WRITE': permission.can_edit,
                'DELETE': permission.can_delete
            }

            has_permission = actions_mapping.get(action)
            if has_permission is None or not has_permission:
                return HttpResponseForbidden("You do not have permission to perform this action.")

            return view_func(view, request, *args, **kwargs)

        return _wrapped_view
    return decorator
