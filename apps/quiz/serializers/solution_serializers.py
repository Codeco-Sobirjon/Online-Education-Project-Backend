from rest_framework import serializers

from apps.quiz.models import QuizSolution


class QuizSolutionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuizSolution
        fields  = ['id', 'sample_question', 'image', 'video']


class QuizSolutionListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuizSolution
        fields  = ['id', 'sample_question']
    