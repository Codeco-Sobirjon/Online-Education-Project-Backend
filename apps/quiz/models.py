import uuid
from django.db import models
from apps.course.models import Course
from config.utils import CustomIDField, CustomAutoField


class QuizSolution(models.Model):
    id = CustomIDField(primary_key=True, editable=False)
    sample_question = models.CharField(max_length=250)
    image = models.ImageField(upload_to='answer/')
    video = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quiz_solution'
        verbose_name = 'Quiz Solution'
        verbose_name_plural = 'Quiz Solutions'
        ordering = ['created_at']

    def __str__(self):
        return self.sample_question or "No Answer"


class QuizGroup(models.Model):
    id = CustomIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=250)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quiz_group'
        verbose_name = 'Quiz Group'
        verbose_name_plural = 'Quiz Groups'
        ordering = ['created_at']

    def __str__(self):
        return self.title


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(QuizGroup, on_delete=models.CASCADE, related_name='quizzes')
    question = models.CharField(max_length=250)
    image = models.ImageField(upload_to='quiz/', null=True, blank=True)
    video = models.URLField(null=True, blank=True)
    solution = models.ForeignKey(QuizSolution, on_delete=models.CASCADE, related_name='quizzes', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quiz'
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
        ordering = ['created_at']

    def __str__(self):
        return self.question


class QuizChoice(models.Model):
    id = CustomAutoField(primary_key=True, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz_choice'
        verbose_name = 'Quiz Choice'
        verbose_name_plural = 'Quiz Choices'
        ordering = ['quiz', 'id']

    def __str__(self):
        return self.text
