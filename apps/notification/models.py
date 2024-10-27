from uuid import uuid4

from django.db import models


class Notification(models.Model):
    class Type(models.TextChoices):
        SPECIAL = 'special', 'Special'
        GENERAL = 'general', 'General'
        PAYMENT = 'payment', 'Payment'
        UPDATE = 'update', 'Update'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    body = models.TextField()
    type = models.CharField(max_length=10, choices=Type.choices)
    image = models.ImageField(upload_to='notification/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
