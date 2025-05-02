import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from users.models import CustomUser
from channels.db import database_sync_to_async
from urllib.parse import parse_qs


class JwtAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return JwtAuthMiddlewareInstance(scope, self)


class JwtAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.scope = dict(scope)
        self.middleware = middleware

    async def __call__(self, receive, send):
        query_string = self.scope["query_string"].decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        self.scope["user"] = await self.get_user(token)
        inner = self.middleware.inner(self.scope)
        return await inner(receive, send)

    @database_sync_to_async
    def get_user(self, token):
        if not token:
            return AnonymousUser()
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            return CustomUser.objects.get(id=user_id)
        except Exception:
            return AnonymousUser()


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(inner)