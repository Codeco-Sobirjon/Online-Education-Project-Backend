from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.info.filters import FAQFilter
from apps.info.models import FAQCategory, FAQ
from apps.info.serializers.faq_serializers import FAQCategorySerializer, FAQSerializer
from config.permissons import IsAdminOrReadOnly

FAQ_MANUAL_PARAMETERS = [
    OpenApiParameter('search', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description="Searching"),
    OpenApiParameter('category_id', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description="Category ID")
]


class FAQCategoryListView(APIView):
    serializer_class = FAQCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

    @extend_schema(
        tags=['FAQ Category'],
        responses={200: FAQCategorySerializer(many=True)},
        description='Get all FAQ categories'
    )
    def get(self, request):
        categories = FAQCategory.objects.all()
        serializer = FAQCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['FAQ Category'],
        request=FAQCategorySerializer,
        responses={201: FAQCategorySerializer},
        description='Create new FAQ category'
    )
    def post(self, request):
        serializer = FAQCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FAQCategoryDetailView(APIView):
    serializer_class = FAQCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

    @extend_schema(
        tags=['FAQ Category'],
        responses={200: FAQCategorySerializer},
        description='Get FAQ category by id'
    )
    def get(self, request, category_id):
        category = self.get_category(category_id)
        serializer = FAQCategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['FAQ Category'],
        request=FAQCategorySerializer,
        responses={200: FAQCategorySerializer},
        description='Update FAQ category by id'
    )
    def put(self, request, category_id):
        category = self.get_category(category_id)
        serializer = FAQCategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['FAQ Category'],
        responses={204: OpenApiResponse(description='No Content')},
        description='Delete FAQ category by id'
    )
    def delete(self, request, category_id):
        category = self.get_category(category_id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_category(category_id):
        return get_object_or_404(FAQCategory, id=category_id)


class FAQListView(APIView):
    serializer_class = FAQSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @extend_schema(
        tags=['FAQ'],
        responses={200: FAQSerializer(many=True)},
        parameters=FAQ_MANUAL_PARAMETERS,
        description='Get all FAQs'
    )
    def get(self, request):
        faqs = FAQ.objects.all()
        faq_filter = FAQFilter(data=request.GET, request=request, queryset=faqs)
        filtered_faqs = faq_filter.qs if faq_filter.is_valid() else faqs.none()
        serializer = FAQSerializer(filtered_faqs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['FAQ'],
        request=FAQSerializer,
        responses={201: FAQSerializer},
        description='Create new FAQ'
    )
    def post(self, request):
        serializer = FAQSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FAQDetailView(APIView):
    serializer_class = FAQSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @extend_schema(
        tags=['FAQ'],
        responses={200: FAQSerializer},
        description='Get FAQ by id'
    )
    def get(self, request, faq_id):
        faq = self.get_faq(faq_id)
        serializer = FAQSerializer(faq)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['FAQ'],
        request=FAQSerializer,
        responses={200: FAQSerializer},
        description='Update FAQ by id'
    )
    def put(self, request, faq_id):
        faq = self.get_faq(faq_id)
        serializer = FAQSerializer(faq, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['FAQ'],
        responses={204: OpenApiResponse(description='No Content')},
        description='Delete FAQ by id'
    )
    def delete(self, request, faq_id):
        faq = self.get_faq(faq_id)
        faq.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_faq(faq_id):
        return get_object_or_404(FAQ, id=faq_id)
