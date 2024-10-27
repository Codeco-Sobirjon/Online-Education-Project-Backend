import uuid
from django.db import models
from rest_framework.exceptions import ValidationError

from apps.accounts.models import User
from apps.course.models import Course


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='reviews', verbose_name="course", db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reviews', verbose_name="user", db_index=True)

    comment = models.TextField(null=True)
    rating = models.PositiveSmallIntegerField(verbose_name="rating")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")

    class Meta:
        db_table = 'review'
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        ordering = ['created_at']
        unique_together = ('course', 'user')

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5.')

    def __str__(self):
        return '{}: {} - {}'.format(self.user, self.course, self.rating)
