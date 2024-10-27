from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.course.models import CourseBookmark
from config.permissons import IsAuth


class CourseBookmarkView(APIView):
    serializer_class = None
    permission_classes = IsAuth,

    @extend_schema(tags=['Bookmark'], responses={200: OpenApiResponse(description='Bookmarked')})
    def post(self, request, course_id):
        CourseBookmark.objects.get_or_create(user=request.user, course_id=course_id)
        return Response({'message': 'Bookmarked'}, status=status.HTTP_200_OK)

    @extend_schema(tags=['Bookmark'], responses={200: OpenApiResponse(description='Unbookmarked')})
    def delete(self, request, course_id):
        CourseBookmark.objects.filter(user=request.user, course_id=course_id).delete()
        return Response({'message': 'Unbookmarked'}, status=status.HTTP_200_OK)
