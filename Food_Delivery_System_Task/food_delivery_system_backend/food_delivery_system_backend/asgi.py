"""
ASGI config for food_delivery_system_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.notifications import routing
from channels.security.websocket import AllowedHostsOriginValidator
from apps.notifications.middleware import custom_auth

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_system_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        custom_auth(URLRouter(routing.websocket_urlpatterns))
    )
})
