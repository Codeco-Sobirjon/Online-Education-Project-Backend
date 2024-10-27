from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.course.models import Category
from apps.course.serializers.category_serializers import CategorySerializer
from config.permissons import IsAdminOrReadOnly


class CategoryList(APIView):
    serializer_class = CategorySerializer
    permission_classes = IsAdminOrReadOnly,

    @extend_schema(tags=['Category'], responses={200: serializer_class(many=True)})
    def get(self, request):
        categories = Category.objects.prefetch_related('courses')
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Category'], request=serializer_class(), responses={
        201: serializer_class(),
        400: OpenApiResponse(description='Bad request')
    })
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    serializer_class = CategorySerializer
    permission_classes = IsAdminOrReadOnly,

    @extend_schema(tags=['Category'], responses={200: serializer_class()})
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        serializer = self.serializer_class(category, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Category'], request=serializer_class(), responses={200: serializer_class()})
    def put(self, request, category_id):
        category = self.get_category(category_id)
        serializer = self.serializer_class(category, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(tags=['Category'], responses={204: None})
    def delete(self, request, category_id):
        category = self.get_category(category_id)
        category.delete()
        return Response('No Content', status=status.HTTP_204_NO_CONTENT)

    def get_category(self, category_id):
        return get_object_or_404(Category, id=category_id)
