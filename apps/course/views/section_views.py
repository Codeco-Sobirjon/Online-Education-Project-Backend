from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.course.models import Section
from apps.course.serializers.section_serializers import SectionSerializer
from config.permissons import IsAdminOrReadOnly


class SectionList(APIView):
    permission_classes = IsAdminOrReadOnly,
    serializer_class = SectionSerializer

    @extend_schema(tags=['Section'], responses={200: serializer_class(many=True)})
    def get(self, request, course_id):
        sections = Section.objects.filter(course_id=course_id)
        serializer = self.serializer_class(sections, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Section'], request=serializer_class(), responses={201: serializer_class()})
    def post(self, request, course_id):
        serializer = self.serializer_class(data=request.data, context={
            'request': request,
            'course_id': course_id
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SectionDetail(APIView):
    serializer_class = SectionSerializer
    permission_classes = IsAdminOrReadOnly,

    @extend_schema(tags=['Section'], responses={200: serializer_class()})
    def get(self, request, section_id):
        section = self.get_section(section_id)
        serializer = self.serializer_class(section, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Section'], request=serializer_class(), responses={200: serializer_class()})
    def put(self, request, section_id):
        section = self.get_section(section_id)
        serializer = self.serializer_class(section, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=['Section'], responses={204: OpenApiResponse(description='Section deleted')})
    def delete(self, request, section_id):
        section = self.get_section(section_id)
        section.delete()
        return Response({'message': 'Section deleted'}, status=status.HTTP_204_NO_CONTENT)

    def get_section(self, section_id):
        return get_object_or_404(Section, id=section_id)
