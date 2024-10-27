from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.quiz.models import QuizSolution
from apps.quiz.serializers.solution_serializers import QuizSolutionSerializer, QuizSolutionListSerializer
from config.permissons import IsAdmin


class QuizSolutionView(APIView):
    serializer_class = QuizSolutionSerializer
    permission_classes = IsAdmin,

    @extend_schema(tags=['Quiz Solution'], responses={200: QuizSolutionListSerializer(many=True)})
    def get(self, request, course_id):
        answers = QuizSolution.objects.filter(course_id=course_id)
        serializer = QuizSolutionListSerializer(answers, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Quiz Solution'], request=QuizSolutionSerializer(), responses={201: QuizSolutionSerializer()})
    def post(self, request, course_id):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(course_id=course_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizSolutionDetailView(APIView):
    serializer_class = QuizSolutionSerializer
    permission_classes = IsAdmin,

    @extend_schema(tags=['Quiz Solution'], responses={200: QuizSolutionSerializer()})
    def get(self, request, solution_id):
        answer = self.get_answer(solution_id)
        serializer = self.serializer_class(answer, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Quiz Solution'], request=QuizSolutionSerializer(), responses={200: QuizSolutionSerializer()})
    def put(self, request, solution_id):
        answer = self.get_answer(solution_id)
        serializer = self.serializer_class(answer, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=['Quiz Solution'], responses={200: OpenApiResponse(description='Solution deleted')})
    def delete(self, request, solution_id):
        answer = self.get_answer(solution_id)
        answer.delete()
        return Response({'message': 'Solution deleted'}, status=status.HTTP_200_OK)

    def get_answer(self, solution_id):
        return get_object_or_404(QuizSolution, id=solution_id)
