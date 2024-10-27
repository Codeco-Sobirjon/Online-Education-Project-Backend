from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.course.models import CoursePart, PartEnrollment
from config.permissons import IsAuth


class PartEnrollView(APIView):
    serializer_class = None
    permission_classes = IsAuth,

    @extend_schema(tags=['Course Part'], request=None, responses={200: OpenApiResponse(description='Enrolled')})
    def post(self, request, part_id):
        user = request.user
        course_part = get_object_or_404(CoursePart, id=part_id)
        enrollment, _ = PartEnrollment.objects.get_or_create(user=user, part=course_part)
        return Response({'message': 'Enrolled'}, status=status.HTTP_200_OK)
