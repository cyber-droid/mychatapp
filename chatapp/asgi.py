import os
from django.core.asgi import get_asgi_application

# Set the default settings module for the 'DJANGO_SETTINGS_MODULE' environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

# Get the ASGI application
application = get_asgi_application()

# Import the routing configuration after the application is initialized
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

# Define the ASGI application with WebSocket support
application = ProtocolTypeRouter({
    "http": application,
    "websocket": URLRouter(chat.routing.websocket_urlpatterns),
})

