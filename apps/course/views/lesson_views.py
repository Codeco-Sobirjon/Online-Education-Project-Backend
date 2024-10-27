from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.course.models import Lesson, CompletedLesson
from apps.course.serializers.lesson_serializers import LessonSerializer
from config.permissons import IsAdmin, IsAuth, IsAdminOrReadOnly


class LessonList(APIView):
    serializer_class = LessonSerializer
    permission_classes = IsAdminOrReadOnly,

    @extend_schema(tags=['Lesson'], responses={200: serializer_class(many=True)})
    def get(self, request, section_id):
        lessons = Lesson.objects.filter(section_id=section_id)
        serializer = self.serializer_class(lessons, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Lesson'], request=serializer_class(), responses={201: serializer_class()})
    def post(self, request, section_id):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(section_id=section_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonDetail(APIView):
    serializer_class = LessonSerializer
    permission_classes = IsAdminOrReadOnly,

    @extend_schema(tags=['Lesson'], responses={200: serializer_class()})
    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        serializer = self.serializer_class(lesson, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Lesson'], request=serializer_class(), responses={200: serializer_class()})
    def put(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        serializer = self.serializer_class(lesson, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=['Lesson'], responses={200: OpenApiResponse(description='Lesson deleted')})
    def delete(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        lesson.delete()
        return Response('No Content', status=status.HTTP_200_OK)


class LessonComplete(APIView):
    serializer_class = LessonSerializer

    @extend_schema(tags=['Lesson'], responses={200: OpenApiResponse(description='Completed')})
    def post(self, request, lesson_id):
        user = request.user
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        CompletedLesson.objects.create(user=user, lesson=lesson)
        return Response({'message': 'Completed'}, status=status.HTTP_200_OK)
    
    def get_permissions(self):
        return IsAuth(),
