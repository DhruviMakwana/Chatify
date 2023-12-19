from django.urls import path
from chat.consumers import VisibilityStatusConsumer, ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/", VisibilityStatusConsumer.as_asgi()),
    path("ws/chat/message/<int:id>/", ChatConsumer.as_asgi()),
]
