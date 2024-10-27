from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.course.models import Section, Course, CompletedLesson
from apps.course.serializers.lesson_serializers import LessonListSerializer


class SectionSerializer(serializers.ModelSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)
    completed_percentage = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'title', 'completed_percentage', 'duration', 'order', 'lesson_count', 'lessons']
        read_only_fields = ['id', 'duration', 'created_at', 'lessons', 'order']

    @staticmethod
    def validate_course_id(value):
        get_object_or_404(Course, id=value)
        return value

    @extend_schema_field(serializers.IntegerField(min_value=0, max_value=100))
    def get_completed_percentage(self, section):
        user = self.context.get('request').user
        if user.is_anonymous:
            return 0
        lesson_count = section.lesson_count
        completed_lesson_count = CompletedLesson.objects.filter(user=user, lesson__section=section).count()
        return completed_lesson_count * 100 // lesson_count if lesson_count > 0 else 0

    def create(self, validated_data):
        course_id = self.context.get('course_id')
        validated_data['course'] = get_object_or_404(Course, id=course_id)
        return Section.objects.create(**validated_data)


class SectionShortInfo(SectionSerializer):

    class Meta:
        model = Section
        fields = ['id', 'title', 'duration', 'order', 'lesson_count', 'completed_percentage']
