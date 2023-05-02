import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Func, Value, CharField, F, QuerySet

from .models import Message


class ChatAsyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

        # getting last 40 messages
        messages: QuerySet[Message] = await database_sync_to_async(self.get_last_40_messages)()

        # parsing QuerySet to list in order to further json.dumps
        messages_list = json.dumps({"messages": await sync_to_async(list)(messages), "start_connection": True})

        # sending last 40 messages to newly connected user
        await self.send(messages_list)

    def get_last_40_messages(self) -> QuerySet[Message]:
        """
        Returns last 40 messages in the cha in format: {'user__username': str, 'text': str,
        'formatted_date': str)}.
        :return:
        """
        return (
            Message.objects.prefetch_related("user")
            .all()
            .order_by("created_at")
            .values("user__username", "text", "created_at")
            .annotate(
                formatted_date=Func(
                    F("created_at"),
                    Value("HH24:MI"),
                    function="to_char",
                    output_field=CharField(),
                )
            )
            .values("user__username", "text", "formatted_date")[:40]
        )

    async def receive(self, text_data=None, bytes_data=None):
        # sends message to chat only when user is authenticated
        if self.scope["user"].is_authenticated:
            data = json.loads(text_data)
            if data["message"] == "":
                await self.send(
                    json.dumps(
                        {
                            "detail": "error",
                            "error_message": "Виникли помилки при відправленні повідомлення.",
                        }
                    )
                )

            # saving message and sending it to users in group
            message: Message = await database_sync_to_async(self.save_message_to_database)(data["message"])
            message_response = {
                "user__username": message.user.username,
                "text": message.text,
                "formatted_date": message.created_at.strftime("%H:%M"),
            }
            await self.channel_layer.group_send("chat", {"type": "chat_message", "message": message_response})

        # error if user is not logged in
        elif self.scope["user"].is_anonymous:
            await self.send(
                json.dumps(
                    {
                        "detail": "error",
                        "error_message": "Ввійдіть в систему, щоб мати змогу надсилати повідомлення.",
                    }
                )
            )

    def save_message_to_database(self, text_message: str):
        return Message.objects.create(user=self.scope["user"], text=text_message)

    async def chat_message(self, event):
        response = {"detail": "success", "message": event["message"]}
        await self.send(json.dumps(response))

    async def close(self, code=None):
        await self.channel_layer.group_discard("chat", self.channel_name)
        await super().close(code=code)
