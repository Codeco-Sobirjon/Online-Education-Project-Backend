from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissons import IsAdminOrReadOnly
from apps.course.models import Color
from apps.course.serializers.color_serializers import ColorSerializer


class ColorList(APIView):
    serializer_class = ColorSerializer
    permission_classes = IsAdminOrReadOnly,

    @extend_schema(tags=['Color'], responses={200: serializer_class(many=True)})
    def get(self, request):
        colors = Color.objects.all()
        serializer = self.serializer_class(colors, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Color'], request=serializer_class(), responses={201: serializer_class()})
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ColorDetail(APIView):
    serializer_class = ColorSerializer
    permission_classes = IsAdminOrReadOnly,

    @extend_schema(tags=['Color'], responses={200: serializer_class()})
    def get(self, request, color_id):
        color = self.get_color(color_id)
        serializer = self.serializer_class(color, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Color'], request=serializer_class(), responses={200: serializer_class()})
    def put(self, request, color_id):
        color = self.get_color(color_id)
        serializer = self.serializer_class(color, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=['Color'], responses={200: OpenApiResponse(description='Color deleted')})
    def delete(self, request, color_id):
        color = self.get_color(color_id)
        color.delete()
        return Response({'message': 'Color deleted'}, status=status.HTTP_200_OK)

    def get_color(self, color_id):
        return get_object_or_404(Color, id=color_id)
