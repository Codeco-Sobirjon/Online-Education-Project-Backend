from rest_framework import serializers

from apps.accounts.models import User
from apps.notification.models import Notification
from config.utils import TimestampField


class NotificationSerializer(serializers.ModelSerializer):
    created_at = TimestampField(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'title', 'body', 'type', 'image', 'created_at']

    def create(self, validated_data):
        admin_user = self.context.get('request').user
        all_users = User.objects.all()
        for user in all_users:
            Notification.objects.create(user=user, **validated_data)
        return Notification.objects.filter(user=admin_user).first()


class NotificationListSerializer(NotificationSerializer):

    class Meta:
        model = Notification
        fields = ['id', 'title', 'image', 'type', 'created_at']
