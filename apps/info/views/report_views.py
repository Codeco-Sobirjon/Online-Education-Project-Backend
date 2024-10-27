from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.info.models import Report
from apps.info.serializers.report_serializers import ReportSerializer
from config.permissons import IsAuth


class ReportListView(APIView):
    serializer_class = ReportSerializer
    permission_classes = IsAuth,

    @extend_schema(
        tags=['Report'],
        responses={200: serializer_class(many=True)},
        description='Report list'
    )
    def get(self, request):
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Report'],
        request=serializer_class,
        responses={200: serializer_class(many=True)},
        description='Create a report'
    )
    def post(self, request):
        serializer = ReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
