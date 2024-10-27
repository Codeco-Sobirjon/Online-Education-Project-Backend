from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.course.models import CoursePart
from apps.course.serializers.part_serializers import CoursePartSerializer


class CoursePartDetailView(APIView):
    serializer_class = CoursePartSerializer
    permission_classes = AllowAny,

    @extend_schema(tags=['Course Part'], responses={200: serializer_class()})
    def get(self, request, part_id):
        part = get_object_or_404(CoursePart, pk=part_id)
        serializer = self.serializer_class(part, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
