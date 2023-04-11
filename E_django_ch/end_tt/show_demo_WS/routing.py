# chat/routing.py
from django.urls import re_path

from . import consumers

show_demo_websocket_urlpatterns = [
    re_path("show_demo_ws", consumers.ShowDemoConsumer.as_asgi()),
] 