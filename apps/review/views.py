from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.review.models import Review
from apps.review.serializers import ReviewSerializer
from config.permissons import IsAuth, IsAuthor


class ReviewList(APIView):
    serializer_class = ReviewSerializer
    permission_classes = IsAuthenticatedOrReadOnly,

    @extend_schema(tags=['Review'], responses={200: serializer_class(many=True)})
    def get(self, request, course_id):
        reviews = Review.objects.filter(course__id=course_id)
        serializer = self.serializer_class(reviews, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Review'], request=serializer_class(), responses={201: serializer_class()})
    def post(self, request, course_id):
        serializer = ReviewSerializer(data=request.data, context={
            'request': request,
            'course_id': course_id
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    serializer_class = ReviewSerializer
    permission_classes = IsAuthenticatedOrReadOnly, IsAuthor

    @extend_schema(tags=['Review'], responses={200: serializer_class()})
    def put(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewSerializer(review, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=['Review'], responses={200: OpenApiResponse(description='Review deleted')})
    def delete(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        return Response({'message': 'Review deleted'}, status=status.HTTP_200_OK)
