from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from config.utils import TimestampField
from .color_serializers import ColorSerializer
from .part_serializers import CoursePartListSerializer
from ..models import Color, CompletedLesson, Course, Category, Lesson, CoursePart
from apps.accounts.models import User
from apps.accounts.serializers import TeacherSerializer


class CourseListSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    category_name = serializers.CharField(read_only=True, source='category.name')
    duration = serializers.IntegerField(read_only=True)
    enrolled = serializers.SerializerMethodField(read_only=True)
    completed_percentage = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    color1 = ColorSerializer(read_only=True)
    color2 = ColorSerializer(read_only=True)
    created_at = TimestampField(read_only=True, help_text='Course created at timestamp')

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'duration', 'category_name', 'teacher', 'image', 'video',
            'color1', 'color2', 'price', 'discounted_price', 'enrolled', 'completed_percentage', 'average_rating',
            'lesson_count', 'student_count', 'is_fragment', 'created_at',
        ]

    def get_enrolled(self, course) -> bool:
        user = self.context.get('request').user
        return user.is_authenticated and user.enrollments.filter(course=course).exists()

    @extend_schema_field(serializers.IntegerField(min_value=0, max_value=100))
    def get_completed_percentage(self, course):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return 0
        lesson_count = course.lesson_count
        completed_lesson_count = CompletedLesson.objects.filter(user=user, lesson__section__course=course).count()
        return completed_lesson_count * 100 // lesson_count if lesson_count > 0 else 0


class CourseSerializer(CourseListSerializer):
    teacher_id = serializers.UUIDField(write_only=True)
    category_id = serializers.UUIDField(write_only=True)
    color1_id = serializers.UUIDField(write_only=True, source='color1.id')
    color2_id = serializers.UUIDField(write_only=True, source='color2.id')

    color1 = ColorSerializer(read_only=True)
    color2 = ColorSerializer(read_only=True)

    last_available_lesson_id = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.FloatField(min_value=0, max_value=5, read_only=True)
    parts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'category_name', 'category_id', 'teacher_id', 'teacher', 'color1', 'color2',
            'color1_id', 'color2_id', 'image', 'video', 'lesson_price', 'discounted_lesson_price', 'part_lesson_count',
            'price', 'discounted_price', 'duration', 'enrolled', 'average_rating', 'lesson_count', 'student_count',
            'review_count', 'is_fragment', 'completed_percentage', 'last_available_lesson_id', 'parts', 'created_at'
        ]

    @staticmethod
    def validate_category_id(value):
        get_object_or_404(Category, id=value)
        return value

    @staticmethod
    def validate_teacher_id(value):
        get_object_or_404(User, id=value, groups__name='teacher')
        return value

    @staticmethod
    def validate_video(value):
        content_type = value.content_type
        if not content_type.startswith('video'):
            raise serializers.ValidationError('The submitted file is not a video file')
        return value

    @extend_schema_field(CoursePartListSerializer(many=True))
    def get_parts(self, course):
        parts = CoursePart.objects.filter(course=course).select_related('course').prefetch_related('lessons')
        print(parts.query)
        return CoursePartListSerializer(parts, many=True, context=self.context).data

    @extend_schema_field(serializers.UUIDField())
    def get_last_available_lesson_id(self, course):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return None

        last_completed_lesson = user.completed_lessons.filter(lesson__section__course=course).last()
        if last_completed_lesson:
            last_available_lesson = Lesson.objects.filter(section__course=course,
                                                          order__gt=last_completed_lesson.order).first()
        else:
            last_available_lesson = Lesson.objects.filter(section__course=course).first()

        if last_available_lesson and user.part_enrollments.filter(part=last_available_lesson.part).exists():
            return last_available_lesson.id

        return None

    def create(self, validated_data):
        color1_data = validated_data.pop('color1')
        color2_data = validated_data.pop('color2')
        color1 = get_object_or_404(Color, **color1_data)
        color2 = get_object_or_404(Color, **color2_data)
        return Course.objects.create(
            color1=color1,
            color2=color2,
            **validated_data
        )

    def update(self, instance, validated_data):
        color1_data = validated_data.pop('color1', None)
        color2_data = validated_data.pop('color2', None)
        color1 = get_object_or_404(Color, **color1_data) if color1_data else instance.color1
        color2 = get_object_or_404(Color, **color2_data) if color2_data else instance.color2
        validated_data['color1'] = color1
        validated_data['color2'] = color2
        return super().update(instance, validated_data)
