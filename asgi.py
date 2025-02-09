import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from exams.routing import websocket_urlpatterns  # Ensure this path is correct

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_portal.settings")

# This creates the standard Django ASGI application to handle HTTP requests.
django_asgi_app = get_asgi_application()

# Create the Channels application with ProtocolTypeRouter.
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Handle traditional HTTP requests
    "websocket": AuthMiddlewareStack(  # Wrap WebSocket connections with authentication (if needed)
        URLRouter(websocket_urlpatterns)  # Route WebSocket requests based on URL patterns
    ),
})


