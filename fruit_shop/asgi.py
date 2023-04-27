import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from chat import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruit_shop.settings')
django_asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': django_asgi_application,
        'websocket': AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))

    }
)
