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
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        scope["user"] = await get_user(token)
        return await self.app(scope, receive, send)

def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(inner)