import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatAsyncConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add('chat', self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.channel_layer.group_send('chat', {'type': 'chat_message', 'message': data['message']})

    async def chat_message(self, event):
        message = event['message']
        await self.send(message)
