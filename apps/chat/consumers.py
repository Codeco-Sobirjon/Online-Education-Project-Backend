import base64
import json
from urllib.parse import urlunparse

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile
from django.http import HttpRequest

from apps.chat.models import Chat, Message, MessageMedia
from apps.chat.serializers import MessageSerializer


class CustomHttpRequest(HttpRequest):
    def __init__(self, scope):
        super().__init__()
        self.method_scheme = "https" if scope.get('secure') else "http"
        self._host = dict(scope['headers']).get(b'host').decode()

    def build_absolute_uri(self, location=None):
        base_url = urlunparse((self.method_scheme, self._host, '', '', '', ''))
        if location:
            return base_url + location
        return base_url


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat = None
        self.user = None
        self.chat_id = None
        self.room_group_name = None

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat = await self.get_chat(self.chat_id)
        self.user = self.scope['user']

        if not self.chat or not self.scope['user'].is_authenticated:
            await self.close()

        self.room_group_name = 'chat_%s' % self.chat_id
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get('message')
        media_data_list = text_data_json.get('media', None)
        message_type = text_data_json.get('type')
        message = await Message.objects.acreate(
            chat=self.chat,
            sender=self.user,
            content=message_text,
            type=message_type
        )

        if media_data_list:
            for media_data in media_data_list:
                file_str, file_name = media_data['data'], media_data['file_name']
                media_file = ContentFile(base64.b64decode(file_str), name=file_name)
                await MessageMedia.objects.acreate(
                    message=message,
                    file=media_file,
                )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        message_serializer = await sync_to_async(MessageSerializer)(message, context={
            'request': CustomHttpRequest(self.scope)
        })
        message_data = await sync_to_async(lambda: message_serializer.data)()
        await self.send(text_data=json.dumps({
            'message': message_data,
            'user': self.user.email
        }))

    @staticmethod
    async def get_chat(chat_id):
        try:
            return await Chat.objects.aget(id=chat_id)
        except Chat.DoesNotExist:
            return None
