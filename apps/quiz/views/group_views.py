from functools import partial
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiResponse

from apps.quiz.models import QuizGroup
from apps.quiz.serializers.group_serializrs import QuizGroupListSerializer, QuizGroupSerializer
from config.permissons import IsAdmin


class QuizGroupView(APIView):
    serializer_class = QuizGroupListSerializer
    permission_classes = IsAdmin,

    @extend_schema(tags=['Quiz Group'], responses={200: QuizGroupListSerializer(many=True)})
    def get(self, request, course_id):
        groups = QuizGroup.objects.filter(course_id=course_id)
        serializer = self.serializer_class(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(tags=['Quiz Group'], request=QuizGroupListSerializer, responses={
        201: QuizGroupListSerializer,
        400: OpenApiResponse(description="Bad request")
    })
    def post(self, request, course_id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(course_id=course_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class QuizGroupDetailView(APIView):
    serializer_class = QuizGroupSerializer
    permission_classes = IsAdmin,

    @extend_schema(tags=['Quiz Group'], responses={200: QuizGroupSerializer})
    def get(self, request, group_id):
        group = get_object_or_404(QuizGroup, id=group_id)
        serializer = self.serializer_class(group)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(tags=['Quiz Group'], request=QuizGroupSerializer, responses={200: QuizGroupSerializer})
    def put(self, request, group_id):
        group = get_object_or_404(QuizGroup, id=group_id)
        serializer = self.serializer_class(group, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(tags=['Quiz Group'], responses={200: OpenApiResponse(description="Deleted")})
    def delete(self, request, group_id):
        group = get_object_or_404(QuizGroup, id=group_id)
        group.delete()
        return Response({'message': 'Group deleted'}, status=status.HTTP_200_OK)
    