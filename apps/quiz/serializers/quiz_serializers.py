from django.shortcuts import get_object_or_404
from rest_framework import serializers
from apps.quiz.models import Quiz, QuizChoice, QuizSolution
from apps.quiz.serializers.solution_serializers import QuizSolutionSerializer


class QuizChoiceSerializser(serializers.ModelSerializer):
    class Meta:
        model = QuizChoice
        fields = ['id', 'text', 'is_correct']


class QuizSerializer(serializers.ModelSerializer):
    solution_id = serializers.CharField(write_only=True)
    choices = QuizChoiceSerializser(many=True, required=True)
    solution = QuizSolutionSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'question', 'image', 'choices', 'solution', 'solution_id']

    def create(self, validated_data):
        solution_id = validated_data.pop('solution_id')
        solution = get_object_or_404(QuizSolution, id=solution_id)
        choices_data = validated_data.pop('choices')
        quiz = Quiz.objects.create(solution=solution, **validated_data)
        for choice_data in choices_data:
            QuizChoice.objects.create(quiz=quiz, **choice_data)
        return quiz
    
    def update(self, instance, validated_data):
        solution_id = validated_data.pop('solution_id', None)
        choices_data = validated_data.pop('choices', None)
        if solution_id is not None:
            solution = get_object_or_404(QuizSolution, id=solution_id)
            instance.solution = solution
        if choices_data is not None:
            instance.choices.all().delete()
            for choice_data in choices_data:
                QuizChoice.objects.create(quiz=instance, **choice_data)
        return super().update(instance, validated_data)


class QuizListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Quiz
        fields = ['id', 'question']
