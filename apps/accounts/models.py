import uuid
from datetime import date
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):

    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    gender = models.CharField(max_length=6, choices=Gender.choices)
    bio = models.TextField(null=True)
    birth_date = models.DateField(null=True)
    phone_number = models.CharField(max_length=20, null=True, unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_assistant = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ('-created_at',)
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def age(self) -> Optional[int]:
        if self.birth_date:
            today = date.today()
            age = today.year - self.birth_date.year
            if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
                age -= 1
            return age
        return None

    def __str__(self):
        return self.email
