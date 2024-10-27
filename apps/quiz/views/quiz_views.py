from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiResponse

from apps.quiz.models import Quiz
from apps.quiz.serializers.quiz_serializers import QuizSerializer
from config.permissons import IsAdminOrReadOnly


class QuizView(APIView):
    serializer_class = QuizSerializer
    permission_classes = IsAdminOrReadOnly,

    @extend_schema(tags=['Quiz'], responses={200: QuizSerializer(many=True)})
    def get(self, request, group_id):
        quizes = Quiz.objects.filter(group_id=group_id)
        serializer = self.serializer_class(quizes, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Quiz'], request=QuizSerializer, responses={201: QuizSerializer()})
    def post(self, request, group_id):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(group_id=group_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizDetailView(APIView):
    serializer_class = QuizSerializer
    permission_classes = IsAdminOrReadOnly,

    @extend_schema(tags=['Quiz'], responses={200: QuizSerializer})
    def get(self, request, quiz_id):
        quiz = self.get_quiz(quiz_id)
        serializer = self.serializer_class(quiz, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Quiz'], request=QuizSerializer, responses={200: QuizSerializer})
    def put(self, request, quiz_id):
        quiz = self.get_quiz(quiz_id)
        serializer = self.serializer_class(quiz, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=['Quiz'], responses={200: OpenApiResponse(description='Quiz deleted')})
    def delete(self, request, quiz_id):
        quiz = self.get_quiz(quiz_id)
        quiz.delete()
        return Response({'message': 'Quiz deleted'}, status=status.HTTP_204_NO_CONTENT)

    def get_quiz(self, quiz_id):
        return get_object_or_404(Quiz, id=quiz_id)
