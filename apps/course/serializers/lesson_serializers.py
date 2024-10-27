from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.course.models import Video, Lesson, CompletedLesson, Section
from apps.quiz.serializers.group_serializrs import QuizGroupSerializer


class VideoSerializer(serializers.ModelSerializer):
    lesson_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Video
        fields = ('lesson_id', 'video_1080p', 'video_720p', 'video_480p', 'video_360p')

    def create(self, validated_data):
        lesson_id = validated_data.pop('lesson_id')
        lesson = get_object_or_404(Lesson, id=lesson_id)
        return Video.objects.create(lesson=lesson, **validated_data)


class LessonSerializer(serializers.ModelSerializer):
    video_1080p = serializers.URLField(write_only=True, required=False)
    video_720p = serializers.URLField(write_only=True)
    video_480p = serializers.URLField(write_only=True)
    video_360p = serializers.URLField(write_only=True)
    quiz_group_id = serializers.CharField(write_only=True)
    duration = serializers.IntegerField(min_value=1)

    video = VideoSerializer(read_only=True)
    quiz_group = QuizGroupSerializer(read_only=True)
    completed = serializers.SerializerMethodField(read_only=True)
    is_available = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'content', 'order', 'video_1080p', 'video_720p', 'video_480p', 'video_360p', 
            'video', 'duration', 'completed', 'is_open', 'is_available', 'quiz_group', 'quiz_group_id',
        ]
        read_only_fields = ['id', 'order']

    def get_completed(self, lesson) -> bool:
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return CompletedLesson.objects.filter(user=user, lesson=lesson).exists()

    def get_is_available(self, lesson) -> bool:
        if lesson.is_open:
            return True
        user = self.context.get('request').user
        if user.is_anonymous or not user.enrollments.filter(course=lesson.section.course).exists():
            return False
        if lesson.order == 1:
            return True
        return CompletedLesson.objects.filter(
            user=user,
            lesson__section=lesson.section,
            lesson__order=lesson.order - 1
        ).exists()

    @staticmethod
    def validate_section_id(value):
        get_object_or_404(Section, id=value)
        return value

    def create(self, validated_data):
        section_id = validated_data.get('section_id')
        validated_data['section'] = get_object_or_404(Section, id=section_id)
        video_1080p = validated_data.pop('video_1080p', None)
        video_720p = validated_data.pop('video_720p', None)
        video_480p = validated_data.pop('video_480p', None)
        video_360p = validated_data.pop('video_360p', None)
        lesson = Lesson.objects.create(**validated_data)
        video = VideoSerializer(data={
            'lesson_id': lesson.id,
            'video_1080p': video_1080p, 'video_720p': video_720p, 'video_480p': video_480p, 'video_360p': video_360p,
        })
        video.is_valid(raise_exception=True)
        video.save()
        return lesson

    def update(self, instance, validated_data):
        video_data = {
            'video_1080p': validated_data.pop('video_1080p', instance.video.video_1080p),
            'video_720p': validated_data.pop('video_720p', instance.video.video_720p),
            'video_480p': validated_data.pop('video_480p', instance.video.video_480p),
            'video_360p': validated_data.pop('video_360p', instance.video.video_360p)
        }
        video = instance.video
        video_serializer = VideoSerializer(video, data=video_data, context=self.context)
        video_serializer.is_valid(raise_exception=True)
        video_serializer.save()
        return super().update(instance, validated_data)


class LessonListSerializer(LessonSerializer):

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order', 'duration', 'completed', 'is_available']
        read_only_fields = ['id', 'order']
