from django.urls import re_path
from public_chat.consumers import GroupChatRoomConsumer
from private_chat.consumers import ChatRoomConsumer
from notifications.consumers import NotificationConsumer

# websocket_urlpatterns = [
#     re_path(r'^group-chat/(?P<room_name>[\w.-]+)/$',GroupChatRoomConsumer.as_asgi()),
#     re_path(r'^chat/(?P<room_name>[\w.-]+)/$',ChatRoomConsumer.as_asgi()),
#     re_path(r'^$',NotificationConsumer.as_asgi()),
# ]



import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Web_Chat.settings')



from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        # "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter([
                re_path(r'^group-chat/(?P<room_name>[\w.-]+)/$',GroupChatRoomConsumer.as_asgi()),
                re_path(r'^chat/(?P<room_name>[\w.-]+)/$',ChatRoomConsumer.as_asgi()),
                re_path(r'^$',NotificationConsumer.as_asgi()),
            ]))
        ),
    }
)