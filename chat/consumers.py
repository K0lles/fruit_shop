import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatAsyncConsumer(AsyncWebsocketConsumer):
    groups = ['chat']

    async def connect(self):
        await self.channel_layer.group_add('chat', self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.channel_layer.group_send('chat', data['message'])
