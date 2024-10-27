from django.db.models import Sum
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.course.models import Section, CompletedLesson, CoursePart, Lesson
from apps.course.serializers.lesson_serializers import LessonListSerializer


class CoursePartSectionsSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField(read_only=True)
    lesson_count = serializers.SerializerMethodField(read_only=True)
    duration = serializers.SerializerMethodField(read_only=True)
    completed_percentage = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Section
        fields = ('id', 'title', 'completed_percentage', 'duration', 'order', 'lesson_count', 'lessons')

    @extend_schema_field(LessonListSerializer(many=True))
    def get_lessons(self, section):
        lessons = self.context.get('lessons')
        return LessonListSerializer(lessons.filter(section=section), many=True, context=self.context).data

    def get_lesson_count(self, section) -> int:
        lessons = self.context.get('lessons')
        return lessons.filter(section=section).count()

    def get_duration(self, section) -> int:
        lessons = self.context.get('lessons')
        return lessons.filter(section=section).aggregate(duration=Sum('duration'))['duration']

    @extend_schema_field(serializers.IntegerField(min_value=0, max_value=100))
    def get_completed_percentage(self, section):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return 0
        lesson_count = section.lesson_count
        completed_lesson_count = CompletedLesson.objects.filter(user=user, lesson__section=section).count()
        return completed_lesson_count * 100 // lesson_count if lesson_count > 0 else 0


class CoursePartSerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    discounted_price = serializers.SerializerMethodField(read_only=True)
    lesson_count = serializers.SerializerMethodField(read_only=True)
    is_available = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CoursePart
        fields = ('id', 'order', 'price', 'discounted_price', 'lesson_count', 'is_available', 'sections')

    @staticmethod
    def get_lesson_count(part) -> int:
        return part.lessons.count()

    def get_price(self, part) -> int:
        return self.get_lesson_count(part) * part.course.lesson_price

    def get_discounted_price(self, part) -> int:
        if part.course.discounted_lesson_price:
            return self.get_lesson_count(part) * part.course.discounted_lesson_price
        return None

    @extend_schema_field(CoursePartSectionsSerializer(many=True))
    def get_sections(self, part):
        lessons = Lesson.objects.filter(part=part).select_related('section').prefetch_related('section__course')
        self.context['lessons'] = lessons
        section_ids = lessons.values_list('section', flat=True).distinct()
        sections = Section.objects.filter(id__in=section_ids)
        return CoursePartSectionsSerializer(sections, many=True, context=self.context).data

    def get_is_available(self, part) -> bool:
        user = self.context.get('request').user
        return user.is_authenticated and user.part_enrollments.filter(part=part).exists()


class CoursePartListSerializer(CoursePartSerializer):

    class Meta:
        model = CoursePart
        fields = ('id', 'order', 'price', 'discounted_price', 'lesson_count', 'is_available')
