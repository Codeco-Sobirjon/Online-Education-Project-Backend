from django.db import models

from apps.accounts.models import User
from config.utils import CustomIDField


class Chat(models.Model):
    id = CustomIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255, null=True)
    participants = models.ManyToManyField(User, related_name='chats')
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'chats'
        verbose_name = 'chat'
        verbose_name_plural = 'chats'
        ordering = ('-created_at',)


class Message(models.Model):

    class Type(models.TextChoices):
        TEXT = 'text', 'Text'
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        FILE = 'file', 'File'
        VOICE = 'voice', 'Voice'

    id = CustomIDField(primary_key=True, editable=False)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE, db_index=True)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.SET_NULL, null=True, db_index=True)
    content = models.TextField(null=True)
    type = models.CharField(max_length=10, choices=Type)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'messages'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('created_at',)


class MessageMedia(models.Model):
    id = CustomIDField(primary_key=True, editable=False)
    message = models.ForeignKey(Message, related_name='media', on_delete=models.CASCADE, db_index=True)
    file = models.FileField(upload_to='message-media/')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'message_media'
        verbose_name = 'message media'
        verbose_name_plural = 'message medias'
        ordering = ('id',)
