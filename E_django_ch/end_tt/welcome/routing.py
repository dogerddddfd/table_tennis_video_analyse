# chat/routing.py
from django.urls import re_path

from . import consumers

ping_websocket_urlpatterns = [
    re_path("welcome/WSping", consumers.PingConsumer.as_asgi()),
] 