from rest_framework import serializers

from apps.quiz.models import QuizGroup
from apps.quiz.serializers.quiz_serializers import QuizSerializer


class QuizGroupSerializer(serializers.ModelSerializer):
    quizzes = QuizSerializer(many=True, read_only=True)
    
    class Meta:
        model = QuizGroup
        fields = ['id', 'title', 'quizzes']


class QuizGroupListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuizGroup
        fields = ['id', 'title']
