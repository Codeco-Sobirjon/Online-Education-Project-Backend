import uuid

from django.db import models


class Banner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='banner/')
    discount = models.PositiveSmallIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'banner'
        verbose_name = 'banner'
        verbose_name_plural = 'banners'
        ordering = ['-created_at']
