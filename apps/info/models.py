from django.db import models

from apps.accounts.models import User
from apps.course.models import Course
from apps.quiz.models import Quiz
from config.utils import CustomAutoField


class Config(models.Model):
    id = CustomAutoField(primary_key=True, editable=False, start_id=1001)
    key = models.CharField(max_length=255, unique=True)
    value = models.BooleanField(default=False)

    class Meta:
        db_table = 'configs'
        verbose_name = 'config'
        verbose_name_plural = 'configs'
        ordering = 'key',


class FAQCategory(models.Model):
    id = CustomAutoField(primary_key=True, editable=False, start_id=11)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'faq_category'
        verbose_name = 'faq category'
        verbose_name_plural = 'faq categories'
        ordering = 'id',


class FAQ(models.Model):
    id = CustomAutoField(primary_key=True, editable=False, start_id=1001)
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE)
    question = models.CharField(max_length=512)
    answer = models.TextField()

    class Meta:
        db_table = 'faq'
        verbose_name = 'faq'
        verbose_name_plural = 'faqs'
        ordering = 'id',


class Contact(models.Model):
    id = CustomAutoField(primary_key=True, editable=False, start_id=1001)
    name = models.CharField(max_length=128)
    link = models.URLField()

    class Meta:
        db_table = 'contact'
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'
        ordering = 'id',


class Report(models.Model):

    class Type(models.TextChoices):
        COURSE = 'course', 'Course'
        QUIZ = 'quiz', 'Quiz'
        OTHER = 'other', 'Other'

    id = CustomAutoField(primary_key=True, editable=False, start_id=1001)
    type = models.CharField(max_length=10, choices=Type)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    message = models.TextField()
    image = models.ImageField(upload_to='reports', null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reports', null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='reports', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'report'
        verbose_name = 'report'
        verbose_name_plural = 'reports'
        ordering = 'id',
