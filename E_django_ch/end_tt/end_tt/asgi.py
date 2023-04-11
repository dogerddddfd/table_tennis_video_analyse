# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from welcome.routing import ping_websocket_urlpatterns
from upload_video.routing import upload_video_websocket_urlpatterns
from show_demo_WS.routing import show_demo_websocket_urlpatterns

websocket_urlpatterns = ping_websocket_urlpatterns + upload_video_websocket_urlpatterns + show_demo_websocket_urlpatterns


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "end_tt.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

 
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)

# import django_async_stream
# django_async_stream.patch_application(django_asgi_app)