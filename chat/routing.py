from django.urls import re_path

from .consumers import ChatAsyncConsumer


websocket_urlpatterns = [re_path(r"ws/chat/$", ChatAsyncConsumer.as_asgi())]
