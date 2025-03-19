import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

# Ensure Django is fully initialized
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')
import django
django.setup()  # Add this to initialize Django

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})