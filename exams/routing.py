from django.urls import re_path
from .consumers import MinimalChatConsumer

websocket_urlpatterns = [
    re_path(r"^ws/test_portal/?$", MinimalChatConsumer.as_asgi()),
]




