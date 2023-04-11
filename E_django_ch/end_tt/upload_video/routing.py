# chat/routing.py
from django.urls import re_path

from . import consumers

upload_video_websocket_urlpatterns = [
    re_path("/WS_upload_video", consumers.UploadConsumer.as_asgi()),
]