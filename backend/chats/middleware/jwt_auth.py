import jwt
from urllib.parse import parse_qs
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from users.models import CustomUser
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(token):
    if not token:
        return AnonymousUser()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        return CustomUser.objects.get(id=user_id)
    except Exception:
        return AnonymousUser()


class JwtAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return JwtAuthMiddlewareInstance(scope, self.inner)


class JwtAuthMiddlewareInstance:
    def __init__(self, scope, inner):
        self.scope = scope
        self.inner = inner

    async def __call__(self, receive, send):
        query_string = self.scope["query_string"].decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        self.scope["user"] = await get_user(token)
        inner = self.inner(self.scope)
        return await inner(receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(inner)