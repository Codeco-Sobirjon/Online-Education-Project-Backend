from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from config.utils import TimestampField
from .models import Chat, Message, MessageMedia
from ..accounts.models import User
from ..accounts.serializers import UserListSerializer


class MessageMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageMedia
        fields = ['id', 'file']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(read_only=True, source='sender.email')
    media = MessageMediaSerializer(many=True, read_only=True)
    created_at = TimestampField(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'type', 'media', 'created_at']


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = UserListSerializer(many=True, read_only=True)
    created_at = TimestampField(read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'is_group', 'created_at', 'messages']


class ChatListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, help_text='Email of the participant')
    participants = UserListSerializer(many=True, read_only=True)
    created_at = TimestampField(read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'is_group', 'email', 'participants', 'created_at']

    def create(self, validated_data):
        email = validated_data.pop('email')
        participant_user = get_object_or_404(User, email=email)
        chat = Chat.objects.create(name='testing')
        chat.participants.add(participant_user, self.context['request'].user)
        return chat
