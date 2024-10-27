from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.accounts.serializers import UserSerializer
from apps.course.models import Course
from apps.review.models import Review
from config.utils import TimestampField


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    rating = serializers.IntegerField(min_value=0, max_value=5)
    created_at = TimestampField(read_only=True, help_text='Review created at timestamp')

    class Meta:
        model = Review
        fields = ['id', 'comment', 'rating', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        user = self.context.get('request').user
        course_id = self.context.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        return Review.objects.create(user=user, course=course,  **validated_data)

    def validate(self, attrs):
        course_id = self.context.get('course_id')
        user = self.context.get('request').user
        is_post = self.context.get('request').method == 'POST'

        if is_post and Review.objects.filter(course_id=course_id, user=user).exists():
            raise serializers.ValidationError('User already reviewed this course.')

        return attrs
