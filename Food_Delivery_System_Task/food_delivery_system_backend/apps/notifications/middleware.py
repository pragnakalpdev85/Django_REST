# chat/middleware.py
# Custom WebSocket authentication middleware for JWT or token auth

import jwt
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from apps.users.models import User
from urllib.parse import parse_qs
from django.conf import settings
from channels.sessions import CookieMiddleware,SessionMiddleware


User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware for JWT authentication on WebSocket connections.
    Reads token from query string: ws://host/ws/path/?token=<jwt>
    """
    async def __call__(self, scope, receive, send):
        # Parse query string to extract token
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]

        if token:
            # Validate JWT and get user
            scope['user'] = await self.get_user_from_jwt(token)
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_jwt(self, token):
        """Validate JWT token and return user"""
        try:
            # Decode the JWT token
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )

            # Get user from payload
            user_id = payload.get('user_id')
            if user_id:
                return User.objects.get(id=user_id)

        except jwt.ExpiredSignatureError:
            # Token has expired
            pass
        except jwt.InvalidTokenError:
            # Invalid token
            pass
        except User.DoesNotExist:
            # User not found
            pass

        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    """
    Alternative middleware for simple token authentication.
    Uses Django REST Framework tokens or custom token model.
    """

    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token_key = query_params.get('token', [None])[0]

        if token_key:
            scope['user'] = await self.get_user_from_token(token_key)
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token_key):
        """Look up user from auth token"""
        try:
            # Using Django REST Framework's Token model
            from rest_framework.authtoken.models import Token
            token = Token.objects.select_related('user').get(key=token_key)
            return token.user
        except:
            return AnonymousUser()

def custom_auth(inner):
    """
    overrides the custome authentication proccess
    """
    return CookieMiddleware(SessionMiddleware(JWTAuthMiddleware(inner)))