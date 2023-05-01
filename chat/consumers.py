import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Func, Value, CharField, F

from .models import Message


class ChatAsyncConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add('chat', self.channel_name)
        await self.accept()

        # getting last 40 messages
        messages = await database_sync_to_async(self.get_last_40_messages)()

        # parsing QuerySet to list in order to further json.dumps
        messages_list = await sync_to_async(lambda: list(messages))()

        # sending last 40 messages to newly connected user
        await self.send(json.dumps(messages_list))

    def get_last_40_messages(self):
        """
        Returns last 40 messages in the chat.
        :return:
        """
        return Message.objects.prefetch_related('user').all().order_by('created_at') \
                   .values('user__username', 'text', 'created_at') \
                   .annotate(formatted_date=
                        Func(
                            F('created_at'), Value('HH:ii'),
                            function='to_char', output_field=CharField()
                        )
                   ) \
                   .values('user__username', 'text', 'formatted_date')[:40]

    async def receive(self, text_data=None, bytes_data=None):
        # sends message to chat only when user is authenticated
        if self.scope['user'].is_authenticated:
            data = json.loads(text_data)
            if data['message'] == '':
                await self.send(json.dumps({'detail': 'error',
                                            'error_message': 'Виникли помилки при відправленні повідомлення.'}))
            await self.channel_layer.group_send('chat', {'type': 'chat_message', 'message': data['message']})

        # error if user is not logged in
        elif self.scope['user'].is_anonymous:
            await self.send(json.dumps({'detail': 'error',
                                        'error_message': 'Ввійдіть в систему, щоб мати змогу надсилати повідомлення.'}))

    async def chat_message(self, event):
        response = {'detail': 'success', 'message': event['message']}
        await self.send(json.dumps(response))

    async def close(self, code=None):
        await self.channel_layer.group_discard('chat', self.channel_name)
        await super().close(code=code)
