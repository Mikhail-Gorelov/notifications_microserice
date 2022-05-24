"""
ASGI config for src project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

django_asgi_app = get_asgi_application()

"""Imports only after get_asgi_application() and env.
Excluded error like:
django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from main.routing import websocket_urlpatterns as notification_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        'websocket':
            URLRouter(
                notification_urlpatterns,
            ),
    }
)
