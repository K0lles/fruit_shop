import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatAsyncConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add('chat', self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        # sends message to chat only when user is authenticated
        if self.scope['user'].is_authenticated:
            data = json.loads(text_data)
            await self.channel_layer.group_send('chat', {'type': 'chat_message', 'message': data['message']})

        # error if user is not logged in
        elif self.scope['user'].is_anonymous:
            await self.send(json.dumps({'detail': 'error',
                                        'error_message': 'Ввійдіть в систему, щоб мати змогу надсилати повідомлення.'}))

    async def chat_message(self, event):
        response = {'detail': 'success', 'message': event['message']}
        await self.send(json.dumps(response))
