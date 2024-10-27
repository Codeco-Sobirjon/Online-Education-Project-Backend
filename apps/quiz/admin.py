from django.contrib import admin
from apps.quiz.models import QuizSolution, QuizGroup, Quiz, QuizChoice


@admin.register(QuizSolution)
class QuizSolutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sample_question', 'course')


@admin.register(QuizGroup)
class QuizGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'solution', 'group')


@admin.register(QuizChoice)
class QuizChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'text', 'is_correct')






