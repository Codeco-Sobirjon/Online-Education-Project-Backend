from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.banner.models import Banner
from apps.banner.serializers import BannerSerializer
from config.permissons import IsAdminOrReadOnly


class BannerView(APIView):
    serializer_class = BannerSerializer
    permission_classes = IsAdminOrReadOnly,

    @extend_schema(
        tags=['Banner'],
        responses={200: serializer_class(many=True)},
        description="Get all banners"
    )
    def get(self, request):
        banners = Banner.objects.all()
        serializer = self.serializer_class(banners, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Banner'],
        request=serializer_class(),
        responses={201: serializer_class()},
        description="Create new banner"
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
